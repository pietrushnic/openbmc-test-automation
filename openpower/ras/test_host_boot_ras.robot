*** Settings ***
Documentation       This suite tests checkstop operations through BMC using
                    pdbg utility during HOST Boot path.

Resource            ../../lib/openbmc_ffdc.robot
Resource            ../../lib/openbmc_ffdc_utils.robot
Resource            ../../lib/openbmc_ffdc_methods.robot
Resource            ../../openpower/ras/ras_utils.robot
Variables           ../../lib/ras/variables.py
Variables           ../../data/variables.py

Library             DateTime
Library             OperatingSystem
Library             random
Library             Collections

Suite Setup         RAS Suite Setup
Test Setup          RAS Test Setup
Test Teardown       FFDC On Test Case Fail
Suite Teardown      RAS Suite Cleanup

Force Tags          Host_boot_RAS

*** Variables ***
${stack_mode}       normal

*** Test Cases ***
Verify Recoverable Callout Handling For MCA At Host Boot

    [Documentation]  Verify recoverable callout handling for MCACALIFIR
    ...              using pdbg tool during Host Boot path.
    [Tags]  Verify_Recoverable_Callout_Handling_For_MCA_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  MCACALIFIR_RECV1
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}mcacalfir_th1

    Inject Error At HOST Boot Path  ${value[0]}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}

*** Comments ***
#  Memory buffer (MCIFIR) related error injection.

Verify Recoverable Callout Handling For MCI At Host Boot
    [Documentation]  Verify recoverable callout handling for MCI
    ...              using pdbg tool during Host Boot path.
    [Tags]  Verify_Recoverable_Callout_Handling_For_MCI_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  MCI_RECV1
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}mcifir_th1

    Inject Error At HOST Boot Path  ${value[0]}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}


Verify Recoverable Callout Handling For NXDMAENG At Host Boot
    [Documentation]  Verify recoverable callout handling for  NXDMAENG with
    ...              using pdbg tool during Host Boot path.
    [Tags]  Verify_Recoverable_Callout_Handling_For_NXDMAENG_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  NX_RECV1
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}nxfir_th1

    Inject Error At HOST Boot Path  ${value[0]}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}


#  L2FIR related error injection.

Verify Recoverable Callout Handling For L2FIR At Host Boot
    [Documentation]  Verify recoverable callout handling for L2FIR with
    ...              using pdbg tool during Host Boot path.
    [Tags]  Verify_Recoverable_Callout_Handling_For_L2FIR_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  L2FIR_RECV1
    ${translated_fir}=  Fetch FIR Address Translation Value  ${value[0]}  EX
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}l2fir_th1

    Inject Error At HOST Boot Path  ${translated_fir}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}


# On chip controller (OCCFIR) related error injection.

Verify Recoverable Callout Handling For OCC At Host Boot
    [Documentation]  Verify recoverable callout handling for OCCFIR with
    ...              using pdbg tool during Host Boot path.
    [Tags]  Verify_Recoverable_Callout_Handling_For_OCC_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  OCCFIR_RECV1
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}occfir_th1


    Inject Error At HOST Boot Path  ${value[0]}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}

# Nest control vunit (NCUFIR) related error injection.

Verify Pdbg Recoverable Callout Handling For NCUFIR At Host Boot
    [Documentation]  Verify recoverable callout handling for NCUFIR
    ...              using pdbg tool during Host Boot path. 
    [Tags]  Verify_Pdbg_Recoverable_Callout_Handling_For_NCUFIR_At_Host_Boot

    ${value}=  Get From Dictionary  ${ERROR_INJECT_DICT}  NCUFIR_RECV1
    ${translated_fir}=  Fetch FIR Address Translation Value  ${value[0]}  EX
    ${err_log_path}=  Catenate  ${RAS_LOG_DIR_PATH}ncufir_th1

    Inject Error At HOST Boot Path  ${translated_fir}  ${value[1]}
    ...  ${value[2]}  ${err_log_path}
