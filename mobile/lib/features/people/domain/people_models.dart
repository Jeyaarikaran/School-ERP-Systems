import 'package:freezed_annotation/freezed_annotation.dart';

part 'people_models.freezed.dart';
part 'people_models.g.dart';

@freezed
class Student with _$Student {
  const factory Student({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    @JsonKey(name: 'admission_no') required String admissionNo,
    @JsonKey(name: 'full_name') required String fullName,
    @JsonKey(name: 'name_local') String? nameLocal,
    @JsonKey(name: 'date_of_birth') required String dateOfBirth,
    required String gender,
    @JsonKey(name: 'blood_group') String? bloodGroup,
    String? phone,
    String? email,
    @JsonKey(name: 'admission_date') required String admissionDate,
    required String status,
  }) = _Student;

  factory Student.fromJson(Map<String, dynamic> json) =>
      _$StudentFromJson(json);
}

@freezed
class ParentGuardian with _$ParentGuardian {
  const factory ParentGuardian({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    @JsonKey(name: 'full_name') required String fullName,
    required String phone,
    String? email,
  }) = _ParentGuardian;

  factory ParentGuardian.fromJson(Map<String, dynamic> json) =>
      _$ParentGuardianFromJson(json);
}

@freezed
class Staff with _$Staff {
  const factory Staff({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    @JsonKey(name: 'employee_code') required String employeeCode,
    @JsonKey(name: 'staff_type') required String staffType,
    @JsonKey(name: 'full_name') required String fullName,
    String? designation,
    String? department,
    @JsonKey(name: 'joining_date') required String joiningDate,
    required String status,
    String? phone,
    String? email,
  }) = _Staff;

  factory Staff.fromJson(Map<String, dynamic> json) =>
      _$StaffFromJson(json);
}
