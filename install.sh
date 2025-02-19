#!/bin/bash

# Usage:
# chmod +x install.sh
# conda init bash
# bash -l install.sh
# zsh -i install.sh

echo "$HOSTNAME"

install_type=${1:-"desktop"}
read -e -i "$install_type" -p "Machine Type [desktop, server, test]: " install_type

script_path=$(readlink -f "$0")
current_dir=$(dirname "$script_path")
root_dir=$current_dir

# Add channels
echo -e "\nAdding channels"
conda config --append channels conda-forge
conda config --append channels nvidia
conda config --append channels pytorch
echo -e "... Done"

# Update 'base' env
echo -e "\nUpdating 'base' environment:"
conda init bash
conda update -n base -c defaults conda --y
conda update --a --y
pip install --upgrade pip
echo -e "... Done"

# Install 'mon' env
echo -e "\nInstalling 'mon' environment:"
case "$OSTYPE" in
  linux*)
    echo -e "\nLinux / WSL"
    # Create `mon` env
    if [ "$install_type" == "desktop" ]; then
      env_yml_path="${current_dir}/linux.yaml"
    elif [ "$install_type" == "server" ]; then
      env_yml_path="${current_dir}/server.yaml"
    else
      env_yml_path="${current_dir}/linux-test.yaml"
    fi

    if [ "$install_type" == "desktop" ] || [ "$install_type" == "server" ]; then
      if { conda env list | grep 'mon'; } >/dev/null 2>&1; then
        echo -e "\nUpdating 'mon' environment:"
        conda env update --name mon -f "${env_yml_path}"
        echo -e "... Done"
      else
        echo -e "\nCreating 'mon' environment:"
        conda env create -f "${env_yml_path}"
        echo -e "... Done"
      fi
    else
      if { conda env list | grep 'montest'; } >/dev/null 2>&1; then
        echo -e "\nUpdating 'montest' environment:"
        conda env update --name mon -f "${env_yml_path}"
        echo -e "... Done"
      else
        echo -e "\nCreating 'montest' environment:"
        conda env create -f "${env_yml_path}"
        echo -e "... Done"
      fi
    fi

    # Install FFMPEG
    sudo apt-get install ffmpeg
    sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
    ;;
  darwin*)
    echo -e "\nMacOS"
    # Must be called before installing PyTorch Lightning
    export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
    export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
    # Create `mon` env
    env_yml_path="${current_dir}/mac.yaml"
    if { conda env list | grep 'mon'; } >/dev/null 2>&1; then
      echo -e "\nUpdating 'mon' environment:"
      conda env update --name mon -f "${env_yml_path}"
      echo -e "... Done"
    else
      echo -e "\nCreating 'mon' environment:"
      conda env create -f "${env_yml_path}"
      echo -e "... Done"
    fi
    # Install FFMPEG
    brew install ffmpeg
    ;;
  win*)
    echo -e "\nWindows"
    # Create `mon` env
    env_yml_path="${current_dir}/linux.yaml"
    if { conda env list | grep 'mon'; } >/dev/null 2>&1; then
      echo -e "\nUpdating 'mon' environment:"
      conda env update --name mon -f "${env_yml_path}"
      echo -e "... Done"
    else
      echo -e "\nCreating 'mon' environment:"
      conda env create -f "${env_yml_path}"
      echo -e "... Done"
    fi
    ;;
  msys*)
    echo -e "\nMSYS / MinGW / Git Bash"
    ;;
  cygwin*)
    echo -e "\nCygwin"
    ;;
  bsd*)
    echo -e "\nBSD"
     ;;
  solaris*)
    echo -e "\nSolaris"
    ;;
  *)
    echo -e "\nunknown: $OSTYPE"
    ;;
esac

echo -e "\nInstall third-party library"
rm -rf poetry.lock
rm -rf $CONDA_PREFIX/lib/python3.10/site-packages/cv2/qt/plugins
eval "$(conda shell.bash hook)"
if [ "$install_type" == "test" ]; then
  conda activate mon
else
  conda activate montest
fi
poetry install --extras "dev"
# poetry install --with dev
# pip install -U openmim
# mim install mmcv-full==1.7.0
conda install cudatoolkit=11.8 --y
conda update --a --y
conda clean --a --y

# Set environment variables
# shellcheck disable=SC2162
echo -e "\nSetting DATA_DIR"
data_dir="/data"
if [ ! -d "$data_dir" ];
then
  data_dir="${root_dir}/data"
fi
read -e -i "$data_dir" -p "Enter DATA_DIR=" input
data_dir="${input:-$data_dir}"
if [ "$data_dir" != "" ]; then
  export DATA_DIR="$data_dir"
  conda env config vars set data_dir="$data_dir"
  echo -e "\nDATA_DIR has been set to $data_dir."
else
  echo -e "\nDATA_DIR has NOT been set."
fi
if [ -d "$root_dir" ];
then
  echo -e "\nDATA_DIR=$data_dir" > "${root_dir}/pycharm.env"
fi
echo -e "... Done"

# Setup Resilio Sync
rsync_dir="${root_dir}/.sync"
mkdir -p "${rsync_dir}"
cp "IgnoreList" "${rsync_dir}/IgnoreList"
echo -e "... Done"
