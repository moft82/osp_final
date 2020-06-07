#! /bin/bash
function md(){ # making directory
    echo "creating dirs..."
    mkdir $1
    cd $1
    mkdir templates
    mkdir static
    cd ..
}
function installing(){ # install python3-pip, curl, bs4 and so on
    echo "update and upgrade..."
    sudo apt-get update
    sudo apt-get upgrade
    echo "installing python3-pip..."
    sudo apt-get install python3-pip
    echo "installing curl..."
    sudo apt install curl
    echo "installing bs4..."
    pip3 install bs4
    echo "installing requests..."
    pip3 install requests
    echo "installing flask..."
    pip3 install flask
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

d=osp # name of directory

if [ ! -d $d ]; then # check if dir is already exsist
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
# check if programs are already downloaded.
# gathering files in zipped file.(if there are files under dir in zip file)

# comment here
#