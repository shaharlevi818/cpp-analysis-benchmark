/**
 * simple_leak.cpp
 * * Purpose: A simple test case for Memory Leak detection.
 * Expected Bug: Memory leak at the allocation line.
 */

#include <iostream>

void cause_memory_leak() {
    int* data = new int[10];

    data[0] = 42;
    std::cout << "Allocated data[0] = " << data[0] << std::endl;

    // BUG: Missing 'delete[] data;' here!
}

int main() {
    std::cout << "Starting memory leak test..." << std::endl;
    cause_memory_leak();
    std::cout << "Test finished." << std::endl;
    return 0;
}