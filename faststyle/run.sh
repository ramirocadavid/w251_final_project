inotifywait -m ./faststyle-master/w251models/ -e create -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        # do something with the file
        STYLENAME=${file%.*}
        pkill -f "python3"
        nohup python3 ./faststyle-master/stylize_webcam.py --model_path ./faststyle-master/models/$STYLENAME --resolution 300 300 &>/dev/null &

    done

