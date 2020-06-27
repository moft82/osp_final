#! /bin/bash

function makeDir(){ # making directory
    echo "creating dirs..."
    mkdir $1
    cd $1
    mkdir templates
    mkdir static
    cd static
    mkdir css
    mkdir js
    mkdir img
    cd ..
    cd ..
}

function moveFile(){ # unzip and move files
    # file="files.tar"
    # echo "unzip file..."
    # tar -xvf $file
    echo "moving files..."
    mv *.py $1
    mv *.htm $1/templates
    mv *.css $1/static/css
    mv *.css.map $1/static/css
    mv *.js $1/static/js
    mv *.js.map $1/static/js
    mv *.jpg $1/static/img
}

function install(){ # install python3-pip, curl, bs4 and so on
    read -p "Do you want to update and upgrade packages? (y/n)? : " answer #check if update and upgrade package
    if [ $answer = 'y' ]; then
        echo "update and upgrade..."
        sudo apt-get update
        sudo apt-get upgrade  
    fi

    dpkg -l | grep python3-pip          # check if python3-pip is installed
    if [ $? == 0 ]; then
        echo "python3-pip is already installed"
    else
        echo "installing python3-pip..." 
        sudo apt-get install python3-pip
    fi

    dpkg -l | grep curl                 # check if curl is installed
    if [ $? == 0 ]; then
        echo "crul is already installed"
    else
        echo "installing curl..."
        sudo apt install curl
    fi

    python3 -c 'import bs4'             # check if bs4 is insatlled
    pipInstall $? bs4 
    python3 -c 'import requests'        # check if requests is insatlled
    pipInstall $? requests
    python3 -c 'import flask'           # check if flask is insatlled
    pipInstall $? flask
    python3 -c 'import wrkzeug'         # check if wrkzeug is insatlled
    pipInstall $? werkzeug
    python3 -c 'import nltk'            # check if nltk is insatlled
    pipInstall $? nltk
    python3 -c 'import numpy'           # check if numpy is insatlled
    pipInstall $? nltk
    python3 -c 'import elasticsearch'   # check if elasticsearch is insatlled
    pipInstall $? elasticsearch
    python3 setting.py                  # downloading nltk, nltk.download("") through setting.py
}

function pipInstall(){
    if [ $1 == 0 ]; then
        echo "$2 is already installed"
    else
        echo "install $2 ..."
        pip3 install $2
    fi
}

function installElasticsearch(){ 
    echo "downloadding elasticsearch"
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-amd64.deb
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-amd64.deb.sha512
    shasum -a 512 -c elasticsearch-7.6.2-amd64.deb.sha512 
    sudo dpkg -i elasticsearch-7.6.2-amd64.deb
}

function serviceStart(){ # run elasticsearch and flask
    echo "run elasticsearch..."
    sudo -i service elasticsearch start
    cd $1
    echo "run flask..."
    flask run
}


d=crawl                     # name of directory
if [ ! -d $d ]; then        # check if dir is already exsist
makeDir $d
else
echo "dir is already exsist."
read -p "Do you want to make dir after removing the exitsting dir (y/n)? : " answer
    if [ $answer = 'y' ]; then
    echo "removing dirs..."
    rm -r $d
    makeDir $d
    else
    exit 0
    fi
fi
read -p "Do you want to install elasticsearch (y/n)? : " answer
if [ $answer = 'y' ]; then
    installElasticsearch
    fi
install
moveFile $d
serviceStart $d
