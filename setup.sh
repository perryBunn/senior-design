pip --version | read message


if [[ $1 == "dev" ]]; then
	echo "******************************"
	echo "*            DEV             *"
	echo "******************************"
	file="./requirements/dev.txt";
else
	file="./requirements/prod.txt"
fi


match="^.*python 3\.[1-9].*"
if [[ $message == *$match* ]]; then
	echo "******************************"
	echo "*         using pip          *"
	echo "******************************"

	pip install -r $file
else
	echo "******************************"
	echo "*        using pip3          *"
	echo "******************************"

	pip3 install -r $file
fi

echo "*******************************************"
echo "Assuming no errors you can run the program."
echo "*******************************************"
