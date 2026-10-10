import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class LibraryScreen extends ConsumerWidget {
  const LibraryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Digital Library'),
        backgroundColor: Colors.blueGrey[700],
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            color: Colors.blueGrey[50],
            child: Center(
              child: Column(
                children: [
                  const Text('Your Library QR Code', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                  const SizedBox(height: 16),
                  Container(
                    width: 200,
                    height: 200,
                    color: Colors.white,
                    child: const Center(
                      child: Icon(Icons.qr_code_2, size: 150, color: Colors.black87),
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text('Scan this at the librarian desk to issue books.', style: TextStyle(color: Colors.black54)),
                ],
              ),
            ),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const Text('Currently Borrowed', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                ListTile(
                  leading: const Icon(Icons.book, color: Colors.blueGrey),
                  title: const Text('Fundamentals of Physics'),
                  subtitle: const Text('Due: Oct 12, 2026'),
                  trailing: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: Colors.orange[100], borderRadius: BorderRadius.circular(8)),
                    child: Text('2 Days Left', style: TextStyle(color: Colors.orange[800], fontSize: 12)),
                  ),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
