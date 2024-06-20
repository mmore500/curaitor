#pragma once
#ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
#define LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"
#include "Empirical/include/emp/web/UrlParams.hpp"
#include "Empirical/include/emp/web/web.hpp"

#include "Config.hpp"
#include "try_read_config_file.hpp"

namespace llms_for_data_extraction {

void setup_config_web(llms_for_data_extraction::Config & config)  {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(emp::web::GetUrlParams(), specs);
  llms_for_data_extraction::try_read_config_file(config, am);
}

} // namespace llms_for_data_extraction

#endif // #ifndef LLMS_FOR_DATA_EXTRACTION_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
