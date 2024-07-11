#!/bin/bash
if [ "$1" ]; then
	export AWS_PROFILE=$1
	echo -e "\e[34mAWS profile updated"
	echo -e "\e[32mCurrently configured AWS_PROFILE is: $AWS_PROFILE"
else
	echo -e "\e[31mProfile name required"
	echo -e "\e[32mCurrently configured AWS_PROFILE is: $AWS_PROFILE"
fi
