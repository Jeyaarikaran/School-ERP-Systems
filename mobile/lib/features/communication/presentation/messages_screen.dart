import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MessagesScreen extends ConsumerWidget {
  const MessagesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Mock notifications from Celery Outbox
    final List<Map<String, dynamic>> notifications = [
      {
        "title": "Mid-Term Exam Schedule",
        "body": "The schedule for the upcoming Mid-Term Exams has been published.",
        "date": "Oct 5, 09:00 AM",
        "isRead": false,
        "priority": "high",
      },
      {
        "title": "Bus Delay: Route 4",
        "body": "Due to heavy traffic, Route 4 will be delayed by 15 minutes.",
        "date": "Oct 5, 07:30 AM",
        "isRead": true,
        "priority": "normal",
      },
      {
        "title": "Fee Reminder (Q3)",
        "body": "Friendly reminder that Q3 fees are due on Oct 10th.",
        "date": "Oct 4, 11:00 AM",
        "isRead": true,
        "priority": "normal",
      },
    ];

    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Messages & Alerts'),
        backgroundColor: Colors.indigo[600],
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        itemCount: notifications.length,
        itemBuilder: (context, index) {
          final notif = notifications[index];
          return Container(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: notif['isRead'] ? Colors.grey[200]! : Colors.indigo[100]!,
                width: notif['isRead'] ? 1 : 2,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.02),
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              leading: CircleAvatar(
                backgroundColor: notif['priority'] == 'high' ? Colors.red[50] : Colors.indigo[50],
                child: Icon(
                  notif['priority'] == 'high' ? Icons.warning_amber_rounded : Icons.notifications_outlined,
                  color: notif['priority'] == 'high' ? Colors.red : Colors.indigo,
                ),
              ),
              title: Text(
                notif['title'],
                style: TextStyle(
                  fontWeight: notif['isRead'] ? FontWeight.w600 : FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(notif['body'], style: const TextStyle(color: Colors.black54)),
                    const SizedBox(height: 8),
                    Text(notif['date'], style: TextStyle(color: Colors.grey[400], fontSize: 12)),
                  ],
                ),
              ),
              trailing: notif['isRead'] 
                  ? null 
                  : Container(
                      width: 12,
                      height: 12,
                      decoration: const BoxDecoration(color: Colors.indigo, shape: BoxShape.circle),
                    ),
            ),
          );
        },
      ),
    );
  }
}
