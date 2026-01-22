cmake_minimum_required(VERSION 3.10)
project(CppAnalysisBenchmark)

add_executable(vulnerable_test vulnerable.cpp)

add_executable(leak_test simple_leak.cpp)