#! /bin/bash

function md(){ # making directory
    echo "creating dirs..."
    mkdir $1
    cd $1
    mkdir templates
    mkdir static
    cd ..
}

function mvfiles(){ # unzip and move files
    file="files.tar"
    echo "unzip file..."
    tar -xvf $file
    echo "moving files..."
    mv files/*.py osp
    mv files/*.htm osp/templates
    mv files/*.css osp/static
    mv files/*.js osp/static
}

function installing(){ # install python3-pip, curl, bs4 and so on
    read -p "Do you want to update and upgrade packages? (y/n)? : " answer #check if update and upgrade package
    if [ $answer = 'y' ]; then
        echo "update and upgrade..."
        sudo apt-get update
        sudo apt-get upgrade  
    fi

    dpkg -l | grep python3-pip  # check if python3-pip is installed
    if [ $? == 0 ]; then
        echo "python3-pip is already installed"
    else
        echo "installing python3-pip..." 
        sudo apt-get install python3-pip
    fi

    dpkg -l | grep curl         # check if curl is installed
    if [ $? == 0 ]; then
        echo "crul is already installed"
    else
        echo "installing curl..."
        sudo apt install curl
    fi

    python3 -c 'import bs4'     # check if bs4 is insatlled
    pipinstall $? bs4 
    python3 -c 'import requests'# check if requests is insatlled
    pipinstall $? requests
    python3 -c 'import flask'          # check if flask is insatlled
    pipinstall $? flask
    python3 -c 'import wrkzeug'          # check if flask is insatlled
    pipinstall $? werkzeug
}

function pipinstall(){ # check if module is installed
    if [ $1 == 0 ]; then
        echo "$2 is already installed"
    else
        echo "install $2 ..."
        pip3 install $2
    fi
}

function installelasticsearch(){ # install elasticsearch tar file and unzip
    echo "downloadding elasticsearch"
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-linux-x86_64.tar.gz
    echo "tar"
    tar xvzf elasticsearch-7.7.1-linux-x86_64.tar.gz
    rm xvzf elasticsearch-7.7.1-linux-x86_64.tar.gz
}

function servicestart(){ # run elasticsearch and flask
    echo "run elasticsearch in background..."
    ./elasticsearch-7.6.2/bin/elasticsearch -d
    echo "run flask..."
    run flask
}


d=osp                   # name of directory
if [ ! -d $d ]; then    # check if dir is already exsist
md $d
else
echo "dir is already exsist."
read -p "Do you want to make dir after removing the exitsting dir (y/n)? : " answer
    if [ $answer = 'y' ]; then
    echo "removing dirs..."
    rm -r $d
    md $d
    else
    exit 0
    fi
fi

installing
mvfiles

# to do list
# gathering files in zipped file.(if there are files under dir in zip file)

# comment here
#