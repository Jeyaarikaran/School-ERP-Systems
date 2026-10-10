import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        backgroundColor: Colors.indigo[600],
        foregroundColor: Colors.white,
        title: const Text('EduCore', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildWelcomeCard(),
            const SizedBox(height: 24),
            const Text(
              'Quick Actions',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87),
            ),
            const SizedBox(height: 16),
            _buildActionGrid(context),
            const SizedBox(height: 24),
            const Text(
              'Today\'s Schedule',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black87),
            ),
            const SizedBox(height: 16),
            _buildScheduleList(),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: 0,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.calendar_today), label: 'Timetable'),
          NavigationDestination(icon: Icon(Icons.message), label: 'Messages'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _buildWelcomeCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.indigo[600]!, Colors.indigo[400]!],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.indigo.withOpacity(0.3),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 30,
            backgroundColor: Colors.white24,
            child: Icon(Icons.person, size: 36, color: Colors.white),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text(
                  'Good Morning,',
                  style: TextStyle(color: Colors.white70, fontSize: 14),
                ),
                Text(
                  'Mr. Aarav Patel',
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 4),
                Text(
                  'Class Teacher - 10A',
                  style: TextStyle(color: Colors.white70, fontSize: 14),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionGrid(BuildContext context) {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 16,
      crossAxisSpacing: 16,
      childAspectRatio: 1.5,
      children: [
        _buildActionCard(
          context: context,
          title: 'Mark Attendance',
          icon: Icons.how_to_reg,
          color: Colors.teal,
          onTap: () {}, // Navigate to offline-first attendance
        ),
        _buildActionCard(
          context: context,
          title: 'Enter Marks',
          icon: Icons.analytics,
          color: Colors.orange,
          onTap: () {
            context.push('/marks');
          },
        ),
        _buildActionCard(
          context: context,
          title: 'Homework',
          icon: Icons.menu_book,
          color: Colors.purple,
          onTap: () {
            context.push('/homework');
          },
        ),
        _buildActionCard(
          context: context,
          title: 'Leave Requests',
          icon: Icons.event_busy,
          color: Colors.red,
          onTap: () {
            context.push('/leave');
          },
        ),
        _buildActionCard(
          context: context,
          title: 'Pay Fees',
          icon: Icons.payment,
          color: Colors.emerald,
          onTap: () {
            context.push('/fees');
          },
        ),
        _buildActionCard(
          context: context,
          title: 'Bus Manifest',
          icon: Icons.directions_bus,
          color: Colors.amber,
          onTap: () {
            context.push('/manifest');
          },
        ),
        _buildActionCard(
          context: context,
          title: 'Library',
          icon: Icons.local_library,
          color: Colors.blueGrey,
          onTap: () {
            context.push('/library');
          },
        ),
      ],
    );
  }

  Widget _buildActionCard({required BuildContext context, required String title, required IconData icon, required Color color, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey[200]!),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const Spacer(),
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.black87),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildScheduleList() {
    return Column(
      children: [
        _buildScheduleItem('08:30 AM', 'Mathematics', 'Class 10-A', true),
        _buildScheduleItem('09:30 AM', 'Physics', 'Class 11-B', false),
        _buildScheduleItem('11:00 AM', 'Free Period', 'Staff Room', false),
      ],
    );
  }

  Widget _buildScheduleItem(String time, String subject, String location, bool isActive) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isActive ? Colors.indigo[50] : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isActive ? Colors.indigo[200]! : Colors.grey[200]!),
      ),
      child: Row(
        children: [
          SizedBox(
            width: 80,
            child: Text(
              time,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: isActive ? Colors.indigo[700] : Colors.grey[600],
              ),
            ),
          ),
          Container(
            width: 4,
            height: 40,
            decoration: BoxDecoration(
              color: isActive ? Colors.indigo[500] : Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
            margin: const EdgeInsets.symmetric(horizontal: 16),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  subject,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: isActive ? Colors.indigo[900] : Colors.black87,
                  ),
                ),
                Text(
                  location,
                  style: TextStyle(color: Colors.grey[600], fontSize: 13),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
