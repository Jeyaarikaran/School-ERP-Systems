import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class LeaveScreen extends ConsumerWidget {
  const LeaveScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Leave Requests'),
        backgroundColor: Colors.red[600],
        foregroundColor: Colors.white,
      ),
      body: const Center(
        child: Text('Leave Application Form UI'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        backgroundColor: Colors.red[600],
        child: const Icon(Icons.add),
      ),
    );
  }
}
