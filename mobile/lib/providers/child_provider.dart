import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final sharedPreferencesProvider = Provider<SharedPreferences>((ref) {
  throw UnimplementedError('Initialize in main()');
});

class SelectedChildNotifier extends StateNotifier<String?> {
  final SharedPreferences prefs;

  SelectedChildNotifier(this.prefs) : super(prefs.getString('selected_child_id'));

  void setChild(String childId) {
    state = childId;
    prefs.setString('selected_child_id', childId);
    // Clearing child-specific caches would happen by other providers watching this state.
  }

  void clear() {
    state = null;
    prefs.remove('selected_child_id');
  }
}

final selectedChildProvider = StateNotifierProvider<SelectedChildNotifier, String?>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SelectedChildNotifier(prefs);
});
