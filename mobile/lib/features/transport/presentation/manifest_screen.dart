import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ManifestScreen extends ConsumerWidget {
  const ManifestScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Route Manifest: Bus 4'),
        backgroundColor: Colors.amber[700],
        foregroundColor: Colors.white,
      ),
      body: ListView(
        children: [
          _buildStop('Stop 1: Maple Street', ['Aarav Patel', 'Diya Sharma'], true),
          _buildStop('Stop 2: Oak Avenue', ['Hari Student'], false),
        ],
      ),
    );
  }

  Widget _buildStop(String stopName, List<String> students, bool isCompleted) {
    return ExpansionTile(
      leading: Icon(isCompleted ? Icons.check_circle : Icons.directions_bus, color: isCompleted ? Colors.green : Colors.amber[700]),
      title: Text(stopName, style: TextStyle(fontWeight: FontWeight.bold, decoration: isCompleted ? TextDecoration.lineThrough : null)),
      children: students.map((s) => ListTile(
        title: Text(s),
        trailing: Switch(value: isCompleted, onChanged: (v){}),
      )).toList(),
    );
  }
}
