import 'dart:async';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthInterceptor extends Interceptor {
  final Dio _dio;
  final FlutterSecureStorage _storage;
  bool _isRefreshing = false;
  Completer<String?>? _refreshTokenCompleter;

  AuthInterceptor(this._dio, this._storage);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await _storage.read(key: 'access_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    // Add request ID
    options.headers['X-Request-ID'] = DateTime.now().millisecondsSinceEpoch.toString();
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      // Single-flight refresh logic
      if (!_isRefreshing) {
        _isRefreshing = true;
        _refreshTokenCompleter = Completer<String?>();

        try {
          final refreshToken = await _storage.read(key: 'refresh_token');
          if (refreshToken == null) throw Exception("No refresh token");

          // Call refresh endpoint
          final response = await _dio.post(
            '/api/v1/auth/refresh', 
            data: {'refresh_token': refreshToken},
            options: Options(headers: {'Authorization': null}), // Don't use expired access token
          );

          if (response.statusCode == 200 && response.data['success']) {
            final newAccess = response.data['data']['access_token'];
            final newRefresh = response.data['data']['refresh_token'];
            
            await _storage.write(key: 'access_token', value: newAccess);
            await _storage.write(key: 'refresh_token', value: newRefresh);
            
            _refreshTokenCompleter?.complete(newAccess);
          } else {
            throw Exception("Refresh failed");
          }
        } catch (e) {
          _refreshTokenCompleter?.complete(null);
          await _storage.deleteAll(); // Wipe on failure
        } finally {
          _isRefreshing = false;
        }
      }

      final newToken = await _refreshTokenCompleter?.future;
      if (newToken != null) {
        // Retry the original request
        final opts = err.requestOptions;
        opts.headers['Authorization'] = 'Bearer $newToken';
        
        try {
          final response = await _dio.fetch(opts);
          return handler.resolve(response);
        } on DioException catch (e) {
          return handler.next(e);
        }
      } else {
        // Redirect to login handled by outer router listener
        return handler.next(err);
      }
    }

    return handler.next(err);
  }
}
