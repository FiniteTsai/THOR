#pragma once

#include "config_file.h"
#include "esp.h"
#include "planet.h"
#include "storage.h"

class phy_module_base
{
public:
    phy_module_base() {};

    ~phy_module_base() {};


    virtual bool initialise_memory(const ESP& esp)                         = 0;
    virtual bool initial_conditions(const ESP& esp, const XPlanet& planet) = 0;

    // TBD, how does it get data? friend of ESP ? grid ?
    virtual bool loop(ESP&   esp,
                      int    nstep,          // Step number
                      int    core_benchmark, // Held-Suarez test option
                      double time_step,      // Time-step [s]
                      double Omega,          // Rotation rate [1/s]
                      double Cp,             // Specific heat capacity [J/kg/K]
                      double Rd,             // Gas constant [J/kg/K]
                      double mu,             // Atomic mass unit [kg]
                      double kb,             // Boltzmann constant [J/K]
                      double P_Ref,          // Reference pressure [Pa]
                      double Gravit,         // Gravity [m/s^2]
                      double A               // Planet radius [m]);
                      ) = 0;


    virtual bool store(const ESP& esp, storage& s) = 0;

    virtual bool configure(config_file& config_reader) = 0;

    virtual bool free_memory() = 0;
};
