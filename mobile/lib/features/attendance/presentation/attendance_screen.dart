import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';
import '../../../core/storage/database.dart';
// Note: In real app, AppDatabase is injected via Riverpod

class AttendanceScreen extends ConsumerStatefulWidget {
  const AttendanceScreen({super.key});

  @override
  ConsumerState<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends ConsumerState<AttendanceScreen> {
  // Mocking the loaded local Drift DB state
  final List<Map<String, dynamic>> _roster = [
    {"id": "1", "name": "Aarav Patel", "status": "present"},
    {"id": "2", "name": "Diya Sharma", "status": "present"},
    {"id": "3", "name": "Rohan Iyer", "status": "present"},
  ];
  
  bool _isOffline = true; // Simulating offline mode

  void _markStatus(int index, String status) {
    setState(() {
      _roster[index]["status"] = status;
    });
  }

  void _submitOfflineQueue() async {
    // 1. AppDatabase creates a local operation with a unique clientOpId
    final clientOpId = const Uuid().v4();
    
    final payload = {
      "client_op_id": clientOpId,
      "section_id": "10-A",
      "attendance_date": DateTime.now().toIso8601String(),
      "records": _roster.map((s) => {"student_id": s["id"], "status": s["status"]}).toList()
    };

    // In full app: 
    // await db.queueOperation(SyncQueueCompanion(
    //   clientOpId: drift.Value(clientOpId),
    //   operationType: drift.Value('ATTENDANCE_SYNC'),
    //   payloadJson: drift.Value(jsonEncode(payload)),
    // ));

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Saved Locally! Will sync when internet returns.'),
        backgroundColor: Colors.teal[600],
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mark Attendance'),
        backgroundColor: Colors.indigo[600],
        foregroundColor: Colors.white,
        actions: [
          if (_isOffline)
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16.0),
              child: Center(
                child: Row(
                  children: [
                    Icon(Icons.cloud_off, size: 16, color: Colors.orangeAccent),
                    SizedBox(width: 4),
                    Text('Offline Mode', style: TextStyle(color: Colors.orangeAccent, fontWeight: FontWeight.bold, fontSize: 12)),
                  ],
                ),
              ),
            ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _roster.length,
        itemBuilder: (context, index) {
          final student = _roster[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    student["name"],
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildStatusButton(index, student["status"], 'present', 'P', Colors.green),
                      _buildStatusButton(index, student["status"], 'absent', 'A', Colors.red),
                      _buildStatusButton(index, student["status"], 'late', 'L', Colors.orange),
                      _buildStatusButton(index, student["status"], 'leave', 'LV', Colors.blue),
                    ],
                  )
                ],
              ),
            ),
          );
        },
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: ElevatedButton(
            onPressed: _submitOfflineQueue,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.indigo[600],
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            child: const Text('Save Register', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusButton(int index, String currentStatus, String targetStatus, String label, Color color) {
    final isSelected = currentStatus == targetStatus;
    return InkWell(
      onTap: () => _markStatus(index, targetStatus),
      child: Container(
        width: 48,
        height: 48,
        decoration: BoxDecoration(
          color: isSelected ? color : Colors.grey[100],
          shape: BoxShape.circle,
          border: Border.all(color: isSelected ? color : Colors.grey[300]!, width: 2),
        ),
        child: Center(
          child: Text(
            label,
            style: TextStyle(
              color: isSelected ? Colors.white : Colors.grey[600],
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}
