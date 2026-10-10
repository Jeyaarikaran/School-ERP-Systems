import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MarksEntryScreen extends ConsumerStatefulWidget {
  const MarksEntryScreen({super.key});

  @override
  ConsumerState<MarksEntryScreen> createState() => _MarksEntryScreenState();
}

class _MarksEntryScreenState extends ConsumerState<MarksEntryScreen> {
  String selectedClass = 'Class 10-A';
  String selectedSubject = 'Mathematics';
  String selectedExam = 'Mid-Term 2026';

  // Mock student list for UI demonstration
  final List<Map<String, dynamic>> students = [
    {'id': 'S001', 'name': 'Hari Student', 'score': 85},
    {'id': 'S002', 'name': 'Aarav Patel', 'score': 92},
    {'id': 'S003', 'name': 'Diya Sharma', 'score': null},
    {'id': 'S004', 'name': 'Rohan Kumar', 'score': 78},
    {'id': 'S005', 'name': 'Ananya Singh', 'score': null},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Enter Marks', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF4F46E5),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.save_outlined),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Marks saved successfully! (Offline Sync enabled)')),
              );
            },
          )
        ],
      ),
      body: Column(
        children: [
          // Filter Section
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))
              ],
            ),
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: _buildDropdown('Class', selectedClass, ['Class 10-A', 'Class 10-B', 'Class 9-A']),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _buildDropdown('Subject', selectedSubject, ['Mathematics', 'Physics', 'Chemistry']),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                _buildDropdown('Exam Type', selectedExam, ['Mid-Term 2026', 'Finals 2026', 'Unit Test 1']),
              ],
            ),
          ),
          
          // Student List Header
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${students.length} Students',
                  style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black54),
                ),
                const Text(
                  'Score / 100',
                  style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black54),
                ),
              ],
            ),
          ),

          // Student List
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              itemCount: students.length,
              itemBuilder: (context, index) {
                final student = students[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(color: Colors.grey[200]!),
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    leading: CircleAvatar(
                      backgroundColor: const Color(0xFF4F46E5).withOpacity(0.1),
                      child: Text(
                        student['name'][0],
                        style: const TextStyle(color: Color(0xFF4F46E5), fontWeight: FontWeight.bold),
                      ),
                    ),
                    title: Text(student['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text('ID: ${student['id']}', style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                    trailing: SizedBox(
                      width: 70,
                      child: TextField(
                        keyboardType: TextInputType.number,
                        textAlign: TextAlign.center,
                        decoration: InputDecoration(
                          hintText: student['score'] != null ? student['score'].toString() : '--',
                          contentPadding: const EdgeInsets.symmetric(vertical: 8),
                          filled: true,
                          fillColor: student['score'] != null ? Colors.green[50] : Colors.grey[100],
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(8),
                            borderSide: BorderSide.none,
                          ),
                        ),
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: student['score'] != null ? Colors.green[700] : Colors.black87,
                        ),
                        onChanged: (val) {
                          // Logic to queue update to drift DB would go here
                        },
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDropdown(String label, String value, List<String> items) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(8),
        border: BorderSide(color: Colors.grey[300]!),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          icon: const Icon(Icons.keyboard_arrow_down, color: Colors.black54),
          style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w600, fontSize: 14),
          onChanged: (String? newValue) {
            if (newValue != null) {
              setState(() {
                if (label == 'Class') selectedClass = newValue;
                if (label == 'Subject') selectedSubject = newValue;
                if (label == 'Exam Type') selectedExam = newValue;
              });
            }
          },
          items: items.map<DropdownMenuItem<String>>((String item) {
            return DropdownMenuItem<String>(
              value: item,
              child: Text(item),
            );
          }).toList(),
        ),
      ),
    );
  }
}
