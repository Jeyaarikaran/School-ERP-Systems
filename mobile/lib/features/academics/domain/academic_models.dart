import 'package:freezed_annotation/freezed_annotation.dart';

part 'academic_models.freezed.dart';
part 'academic_models.g.dart';

@freezed
class ClassLevel with _$ClassLevel {
  const factory ClassLevel({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    required String name,
    required int level,
    @JsonKey(name: 'display_order') required int displayOrder,
  }) = _ClassLevel;

  factory ClassLevel.fromJson(Map<String, dynamic> json) =>
      _$ClassLevelFromJson(json);
}

@freezed
class Section with _$Section {
  const factory Section({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    @JsonKey(name: 'class_id') required String classId,
    @JsonKey(name: 'academic_year_id') required String academicYearId,
    required String name,
    required int capacity,
  }) = _Section;

  factory Section.fromJson(Map<String, dynamic> json) =>
      _$SectionFromJson(json);
}

@freezed
class Subject with _$Subject {
  const factory Subject({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    required String code,
    required String name,
    required String type,
  }) = _Subject;

  factory Subject.fromJson(Map<String, dynamic> json) =>
      _$SubjectFromJson(json);
}

@freezed
class AcademicYear with _$AcademicYear {
  const factory AcademicYear({
    required String id,
    @JsonKey(name: 'school_id') required String schoolId,
    required String name,
    @JsonKey(name: 'start_date') required String startDate,
    @JsonKey(name: 'end_date') required String endDate,
    required String status,
  }) = _AcademicYear;

  factory AcademicYear.fromJson(Map<String, dynamic> json) =>
      _$AcademicYearFromJson(json);
}
