#!/bin/bash
#
# Setup a RAMP backend architecture for a given RAMP project

set -e

# Text management
bold=`tput bold`
normal=`tput sgr0`
underline=`tput smul`

##############
# Script help
##############
usage()
{
  echo "
  ${bold}Setup a RAMP backend architecture for a given RAMP project${normal}

  Usage:

    ${bold}./ubuntu_setup.sh <ramp_kit_name> <ramp_environment_file>${normal}

    where <ramp_kit_name> stands for the name of the RAMP kit on GitHub
        ${underline}https://github.com/ramp-kits/<ramp_kit_name>${normal}
    
    where <ramp_environment_file> is the path to the `ramp_environment.yml`
        provided with this script
    "
}

#-----------------------------------------------------------
# Script variables definition
#-----------------------------------------------------------
project_name="$1"
ramp_dependencies="$2"

RAMPKIT_DIR="$HOME/ramp-kits"
kit_url="https://github.com/ramp-kits/$project_name"
kit_dir="$RAMPKIT_DIR/$project_name"

ami_environment="$kit_dir/ami_environment.yml"
data_dir="$kit_dir/data"

#######################################################
# Batch install of latest Miniconda in $HOME directory
#######################################################
miniconda_install() {
  LATEST_MINICONDA="http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh"
  wget -q $LATEST_MINICONDA -O miniconda.sh
  chmod +x miniconda.sh
  /bin/bash miniconda.sh -b -p

  echo 'export PATH="${HOME}/miniconda3/bin:$PATH"' >> .profile
  source .profile

  conda update --yes --quiet conda
  pip install --upgrade pip
}

#################################################################
# Install Python dependencies in the base conda environment 
#
# Argument:
#   path to a conda environment file (usually 'environment.yml')
#################################################################
update_conda_env() {
    environment_file=$1
    conda env update --name base --file $environment_file
}

#############################################################
# Upgrade the kernal and install conda and RAMP dependencies
#############################################################
system_setup() {
  sudo apt-get upgrade
  miniconda_install
  update_conda_env $ramp_dependencies
}

#################################################################
# Clone the ramp-kit, install dependencies and download the data
#################################################################
project_setup() {
  mkdir $RAMPKIT_DIR
  git clone $kit_url $kit_dir
  update_conda_env $ami_environment
  rm -rf $data_dir && mkdir $data_dir
  echo "\n${bold}==> Last step is to put the backend data into '$data_dir'${normal}\n"
}


start_prompt() {
  echo "\n---------------------------------------------------------------"
  echo " Starting the setup of the RAMP AMI for $project_name project"
  echo "---------------------------------------------------------------\n"
}

end_prompt() {
  echo "\n---------------------------------------------------------------"
  echo " Ending the setup of the RAMP AMI for $project_name project"
  echo "---------------------------------------------------------------\n"
}

#######
# Main
#######
main() {
  if [[ "$project_name" == "" || "$project_name" == "help" ]]; then
    usage
  else
    start_prompt
    system_setup
    project_setup
    end_prompt
  fi
}

main
