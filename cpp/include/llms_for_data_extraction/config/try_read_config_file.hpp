#pragma once
#ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
#define LLMS_FOR_DATA_EXTRACTION_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE

#include <cstdlib>
#include <filesystem>
#include <iostream>

#include "Config.hpp"

namespace llms_for_data_extraction {

void try_read_config_file(llms_for_data_extraction::Config & config, emp::ArgManager & am) {
  if(std::filesystem::exists("llms_for_data_extraction.cfg")) {
    std::cout << "Configuration read from llms_for_data_extraction.cfg" << '\n';
    config.Read("llms_for_data_extraction.cfg");
  }
  am.UseCallbacks();
  if (am.HasUnused())
    std::exit(EXIT_FAILURE);
}

} // namespace llms_for_data_extraction

#endif // #ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
