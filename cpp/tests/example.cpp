#define CATCH_CONFIG_MAIN

#include "Catch/single_include/catch2/catch.hpp"

#include "llms_for_data_extraction/example.hpp"

TEST_CASE("Test example") {
  REQUIRE( llms_for_data_extraction::example() );
}
