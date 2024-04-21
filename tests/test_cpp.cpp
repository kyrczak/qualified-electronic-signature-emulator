#include <iostream>

int main() {
    int size;
    std::cout << "Enter the size of the square: ";
    std::cin >> size;

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            std::cout << "* ";
        }
        std::cout << std::endl;
    }

    return 0;
}