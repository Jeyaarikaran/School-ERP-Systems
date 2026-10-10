import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

// Assuming basic auth state is available from scaffolding
import 'features/auth/presentation/login_screen.dart';
import 'features/dashboard/presentation/dashboard_screen.dart';
import 'features/academics/presentation/marks_entry_screen.dart';
import 'features/academics/presentation/homework_screen.dart';
import 'features/finance/presentation/fees_screen.dart';
import 'features/transport/presentation/manifest_screen.dart';
import 'features/leave/presentation/leave_screen.dart';
import 'features/library/presentation/library_screen.dart';

void main() {
  runApp(
    const ProviderScope(
      child: EduCoreApp(),
    ),
  );
}

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/login',
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/',
        builder: (context, state) => const DashboardScreen(),
      ),
      GoRoute(
        path: '/marks',
        builder: (context, state) => const MarksEntryScreen(),
      ),
      GoRoute(
        path: '/homework',
        builder: (context, state) => const HomeworkScreen(),
      ),
      GoRoute(
        path: '/fees',
        builder: (context, state) => const FeesScreen(),
      ),
      GoRoute(
        path: '/manifest',
        builder: (context, state) => const ManifestScreen(),
      ),
      GoRoute(
        path: '/leave',
        builder: (context, state) => const LeaveScreen(),
      ),
      GoRoute(
        path: '/library',
        builder: (context, state) => const LibraryScreen(),
      ),
      // Future routes for Attendance, Homework, etc.
    ],
    // In production, add redirect logic here based on AuthState
  );
});

class EduCoreApp extends ConsumerWidget {
  const EduCoreApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'EduCore ERP',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF4F46E5), // Indigo 600
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        fontFamily: 'Inter',
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
