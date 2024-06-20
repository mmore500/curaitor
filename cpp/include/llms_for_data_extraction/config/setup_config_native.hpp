#pragma once
#ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
#define LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"

#include "try_read_config_file.hpp"

namespace llms_for_data_extraction {

void setup_config_native(llms_for_data_extraction::Config & config, int argc, char* argv[]) {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(argc, argv, specs);
  llms_for_data_extraction::try_read_config_file(config, am);
}

} // namespace llms_for_data_extraction

#endif // #ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
