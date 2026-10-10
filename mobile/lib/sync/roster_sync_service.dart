import 'dart:async';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../database/database.dart';

final databaseProvider = Provider((ref) => AppDatabase());
final dioProvider = Provider((ref) => Dio());

final rosterSyncServiceProvider = Provider((ref) => RosterSyncService(
      dio: ref.read(dioProvider),
      db: ref.read(databaseProvider),
    ));

class RosterSyncService {
  final Dio dio;
  final AppDatabase db;
  bool _isSyncing = false;

  RosterSyncService({required this.dio, required this.db});

  Future<void> syncRosters() async {
    if (_isSyncing) return;
    _isSyncing = true;

    try {
      final stateQuery = await (db.select(db.syncState)..where((t) => t.id.equals('roster_sync'))).getSingleOrNull();
      String? cursor = stateQuery?.cursor;
      bool hasMore = true;

      while (hasMore) {
        final response = await dio.get('/api/v1/sync/rosters', queryParameters: {
          if (cursor != null) 'cursor': cursor,
        });

        final data = response.data['data'];
        final nextCursor = data['next_cursor'];
        hasMore = data['has_more'] ?? false;
        
        final List<dynamic> upserts = data['upserts'] ?? [];
        final List<dynamic> tombstones = data['tombstones'] ?? [];

        await db.transaction(() async {
          // Process upserts
          for (var item in upserts) {
            // Check if it's a section or student by structure
            if (item.containsKey('class_id')) {
              await db.into(db.localSections).insertOnConflictUpdate(LocalSection(
                id: item['id'],
                name: item['name'],
                classId: item['class_id'],
              ));
            } else if (item.containsKey('section_id')) {
              await db.into(db.localStudents).insertOnConflictUpdate(LocalStudent(
                id: item['id'],
                name: item['name'],
                rollNo: item['roll_no'],
                photoThumbnailKey: item['photo_thumbnail_key'],
                sectionId: item['section_id'],
              ));
            }
          }

          // Process tombstones
          for (var id in tombstones) {
            await (db.delete(db.localStudents)..where((t) => t.id.equals(id))).go();
            await (db.delete(db.localSections)..where((t) => t.id.equals(id))).go();
          }

          // Save cursor inside the same transaction
          if (nextCursor != null) {
            cursor = nextCursor;
            await db.into(db.syncState).insertOnConflictUpdate(SyncStateData(
              id: 'roster_sync',
              cursor: cursor,
              lastSyncedAt: DateTime.now(),
            ));
          }
        });
      }
    } catch (e) {
      print("Roster sync failed: $e");
      // Silently fail to allow offline usage, retry next time
    } finally {
      _isSyncing = false;
    }
  }
}
