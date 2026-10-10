import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../storage/database.dart';

/// Provider for the SyncWorker to be used across the app
final syncWorkerProvider = Provider<SyncWorker>((ref) {
  // Assuming dioProvider and dbProvider are available in real implementation
  return SyncWorker(Dio(), AppDatabase()); 
});

/// Background worker that drains the SyncQueue.
/// Designed for Offline-First Architecture (ADR-009).
class SyncWorker {
  final Dio _dio;
  final AppDatabase _db;
  bool _isSyncing = false;

  SyncWorker(this._dio, this._db);

  /// Called periodically or when network status changes to 'online'
  Future<void> runSync() async {
    if (_isSyncing) return;
    _isSyncing = true;

    try {
      // 1. Fetch pending operations
      final pendingOps = await (_db.select(_db.syncQueue)
            ..where((t) => t.status.equals(0)) // 0 = pending
            ..orderBy([(t) => OrderingTerm(expression: t.createdAt)]))
          .get();

      if (pendingOps.isEmpty) {
        _isSyncing = false;
        return;
      }

      print('Starting sync for ${pendingOps.length} operations...');

      for (final op in pendingOps) {
        await _processOperation(op);
      }

    } finally {
      _isSyncing = false;
    }
  }

  Future<void> _processOperation(SyncQueueData op) async {
    try {
      // Mark as syncing
      await (_db.update(_db.syncQueue)..where((t) => t.id.equals(op.id)))
          .write(const SyncQueueCompanion(status: drift.Value(1)));

      final payload = jsonDecode(op.payloadJson);

      if (op.operationType == 'ATTENDANCE_SYNC') {
        // Idempotency-Key is critical here! Provided by clientOpId
        await _dio.post(
          '/api/v1/attendance/sync',
          data: payload,
          options: Options(headers: {
            'Idempotency-Key': op.clientOpId,
          }),
        );
      }
      
      // If successful, delete the operation from the queue
      await (_db.delete(_db.syncQueue)..where((t) => t.id.equals(op.id))).go();
      print('Successfully synced operation: ${op.clientOpId}');

    } on DioException catch (e) {
      print('Network error syncing op ${op.clientOpId}: ${e.message}');
      
      // If it's a 4xx error, it's a permanent failure (conflict, invalid data)
      if (e.response != null && e.response!.statusCode! >= 400 && e.response!.statusCode! < 500) {
         await (_db.update(_db.syncQueue)..where((t) => t.id.equals(op.id)))
          .write(const SyncQueueCompanion(status: drift.Value(2))); // 2 = failed
      } else {
         // Otherwise (5xx or network timeout), reset to pending for retry
         await (_db.update(_db.syncQueue)..where((t) => t.id.equals(op.id)))
          .write(const SyncQueueCompanion(status: drift.Value(0))); // back to pending
      }
    } catch (e) {
      print('Unexpected error syncing op ${op.clientOpId}: $e');
      await (_db.update(_db.syncQueue)..where((t) => t.id.equals(op.id)))
          .write(const SyncQueueCompanion(status: drift.Value(2))); // failed
    }
  }
}
