#!/usr/bin/env fish

set POSSIBLE_CMDS '--update' '--day' '--clean' '--deep-clean' '--record'

for idx in (seq (count $argv))
    set arg $argv[$idx]
    if not test $arg
        break
    end

    switch $arg
        case --update
            set -g should_update true
            continue
        case --clean
            set -g should_clean true
            continue
        case --deep-clean
            set -g should_deep_clean true
            continue
        case --record
            set -g should_record $argv[(math $idx+1)]
            continue
        case --day
            set -g is_day $argv[(math $idx+1)]
            continue
    end
end

echo '--update:' $should_update
echo '--clean:' $should_clean
echo '--record:' $should_record
echo '--day:' $is_day

set TEMP_FILE (mktemp -t cs251)

set USERS rives
set ALL_USERS $USERS
set stogit 'git@stogit.cs.stolaf.edu:sd-s15'

if set -q is_day
  set -g DATE (date -v1w -v-$is_day "+%Y-%m-%d")
  echo "Checking out last $is_day at 5:00pm"
end

set PROGRESS
set PROGRESS[(count $ALL_USERS)] ''

for idx in (seq 1 (count $PROGRESS))
	set PROGRESS[$idx] ' '
end

cd _users
for idx in (seq (count $ALL_USERS))
	set user $ALL_USERS[$idx]
	set PROGRESS[$idx] '.'
	printf "\r["
	for dot in $PROGRESS; printf "$dot"; end
	printf "] ($user)"

    if set -q should_deep_clean
        rm -rf $user
    end

	if not test -d $user
		git clone --quiet "$stogit/$user.git"
	end
	cd $user

    if set -q should_clean
        git stash -u
        git stash clear
    end

    if set -q should_update
        git pull --rebase --quiet origin master
    end

    if set -q DATE
        git checkout (git rev-list -n 1 --before="$DATE 18:00" master) --force --quiet
    end

    if set -q should_record
        if test -d $should_record
            cd $should_record
            ~/cs251/_scripts/markdownify.py $should_record $user >> ~/cs251/_logs/log-$should_record.md
            cd -
        end
    end

	# pwd
	# for dir in (find . -type d -maxdepth 1 -not -name .git -not -name .)
		# echo $dir
		# mkdir -p ../_homeworks/$dir
		# ln -Ffs ../../$user/$dir ../_homeworks/$dir/$user
		# todo: figure out why this gets created in the first place
		# rm -f $dir/$dir
	# end

	# git status --porcelain

	set FOLDERS (tree -I '.git' --noreport --du -d --prune -i -L 1 | grep '\d\d\d\d*' | awk '{print $3}' | tr [A-Z] [a-z] | tr ' ' '\n' | sort)
	set HWS (echo $FOLDERS | tr ' ' '\n' | grep -i 'hw' | tr '\n' ' ')
	set LABS (echo $FOLDERS | tr ' ' '\n' | grep --invert-match 'hw' | tr '\n' ' ')

	printf "$user\t$HWS\t$LABS\n" >> $TEMP_FILE

    if set -q DATE
        git checkout master --quiet --force
    end

	cd ..
end
cd ..
echo ''

cat $TEMP_FILE | ~/cs251/_scripts/columnize.py
