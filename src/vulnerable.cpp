// src/vulnerable.cpp

#include <iostream>
#include <cstring>

// demonstrate overflow - access outside boundry 
void buffer_overflow_example() {
    char buffer[10];
    strcpy(buffer, "ThisStringIsTooLongForBuffer"); 
}

// dynamic memory allocation without freeing it.
void memory_leak_example() {
    // dynamic allocation (Heap)
    int* ptr = new int[10]; 
    ptr[0] = 100;
    
    // delete[] pre;
}

int main(){
    std::cout << "Starting Vulnerable Application..." << std::endl;
    
    buffer_overflow_example();
    memory_leak_example();

    std::cout << "Finished." << std::endl;
    return 0;
}
