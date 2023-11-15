#include <iostream>

extern "C" 
void print2d(char*** arr, int len, int inner_len)
{
  std::cout << arr << '\n'; //ok
  std::cout.flush(); 
  std::cout << *arr << '\n'; //ok
  std::cout.flush();
  std::cout << **arr << '\n'; //segfaults
  std::cout.flush();
  std::cout << ***arr << '\n';
  std::cout.flush();
  //
  // for(int i = 0; i < len; ++i)
  // {
  //   for(int j = 0; j < inner_len; ++j)
  //   {
  //     std::cout << arr[i][j] << ' ';
  //     std::cout.flush();
  //   }
  //   std::cout.put('\n');
  // }
  for(int i = 0; i < len; ++i)
  {
    for(int j = 0; j < inner_len; ++j)
    {
      std::cout << arr[i]+j << ' ';
      std::cout.flush();
    }
    std::cout.put('\n');
  }
}
