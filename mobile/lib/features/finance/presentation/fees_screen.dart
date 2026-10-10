import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class FeesScreen extends ConsumerWidget {
  const FeesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Fee Payments'),
        backgroundColor: Colors.emerald[600],
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: LinearGradient(colors: [Colors.emerald[600]!, Colors.teal[500]!]),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: const [
                  Text('Total Outstanding', style: TextStyle(color: Colors.white70, fontSize: 16)),
                  SizedBox(height: 8),
                  Text('\$1,250.00', style: TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text('Pending Invoices', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(
              child: ListTile(
                leading: CircleAvatar(backgroundColor: Colors.emerald[50], child: Icon(Icons.receipt, color: Colors.emerald[600])),
                title: const Text('Term 2 Tuition Fee'),
                subtitle: const Text('Due: Oct 15, 2026'),
                trailing: const Text('\$1,200.00', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                // Razorpay SDK Integration goes here
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.emerald[600],
                padding: const EdgeInsets.all(16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text('Pay Now via Razorpay', style: TextStyle(fontSize: 18, color: Colors.white)),
            ),
          ],
        ),
      ),
    );
  }
}
