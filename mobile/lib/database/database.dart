import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'database.g.dart';

class LocalSections extends Table {
  TextColumn get id => text()();
  TextColumn get name => text()();
  TextColumn get classId => text()();
  
  @override
  Set<Column> get primaryKey => {id};
}

class LocalStudents extends Table {
  TextColumn get id => text()();
  TextColumn get name => text()();
  TextColumn get rollNo => text().nullable()();
  TextColumn get photoThumbnailKey => text().nullable()();
  TextColumn get sectionId => text()();

  @override
  Set<Column> get primaryKey => {id};
}

class SyncState extends Table {
  TextColumn get id => text()(); // e.g. "roster_sync"
  TextColumn get cursor => text().nullable()();
  DateTimeColumn get lastSyncedAt => dateTime().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}

@DriftDatabase(tables: [LocalSections, LocalStudents, SyncState])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'db.sqlite'));
    return NativeDatabase.createInBackground(file);
  });
}
