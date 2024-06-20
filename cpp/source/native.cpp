#include <iostream>

#include "Empirical/include/emp/base/vector.hpp"

#include "llms_for_data_extraction/config/Config.hpp"
#include "llms_for_data_extraction/config/setup_config_native.hpp"
#include "llms_for_data_extraction/example.hpp"

// This is the main function for the NATIVE version of LLMs for Data Extraction.

llms_for_data_extraction::Config cfg;

int main(int argc, char* argv[]) {
  // Set up a configuration panel for native application
  setup_config_native(cfg, argc, argv);
  cfg.Write(std::cout);

  std::cout << "Hello, world!" << "\n";

  return llms_for_data_extraction::example();
}
