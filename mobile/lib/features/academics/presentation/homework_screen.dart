import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HomeworkScreen extends ConsumerWidget {
  const HomeworkScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Homework & Assignments'),
        backgroundColor: Colors.purple[600],
        foregroundColor: Colors.white,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildAssignmentCard(
            'Algebra Linear Equations',
            'Mathematics',
            'Due: Tomorrow, 10:00 AM',
            Colors.purple,
          ),
          _buildAssignmentCard(
            'Gravity Experiment Report',
            'Physics',
            'Due: Friday, 02:00 PM',
            Colors.blue,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        backgroundColor: Colors.purple[600],
        icon: const Icon(Icons.camera_alt),
        label: const Text('Upload Work'),
      ),
    );
  }

  Widget _buildAssignmentCard(String title, String subject, String due, MaterialColor color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(subject, style: TextStyle(color: color[700], fontWeight: FontWeight.bold)),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(color: Colors.red[50], borderRadius: BorderRadius.circular(4)),
                  child: Text('Pending', style: TextStyle(color: Colors.red[700], fontSize: 12)),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Row(
              children: [
                Icon(Icons.timer, size: 16, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(due, style: TextStyle(color: Colors.grey[600])),
              ],
            )
          ],
        ),
      ),
    );
  }
}
