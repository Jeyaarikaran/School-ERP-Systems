import 'package:freezed_annotation/freezed_annotation.dart';

part 'auth_state.freezed.dart';
part 'auth_state.g.dart';

@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  
  const factory AuthState.authenticated({
    required String token,
    required User user,
  }) = _Authenticated;
  
  const factory AuthState.unauthenticated({
    String? message,
  }) = _Unauthenticated;
}

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String email,
    required String role,
    @JsonKey(name: 'school_id') required String schoolId,
    @JsonKey(name: 'full_name') required String fullName,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
