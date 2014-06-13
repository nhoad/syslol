Have you ever wanted your error messages in syslog to be more obvious? Or
perhaps you just wished they were a little less boring?

    __   _____  _   _  __        ___    _   _ _____   ______   ______  _     ___  _
    \ \ / / _ \| | | | \ \      / / \  | \ | |_   _| / ___\ \ / / ___|| |   / _ \| |
     \ V / | | | | | |  \ \ /\ / / _ \ |  \| | | |   \___ \\ V /\___ \| |  | | | | |
      | || |_| | |_| |   \ V  V / ___ \| |\  | | |    ___) || |  ___) | |__| |_| | |___
      |_| \___/ \___/     \_/\_/_/   \_\_| \_| |_|   |____/ |_| |____/|_____\___/|_____|


syslol is a syslog daemon that writes any logs with a priority of 4 or below in
the 'big' font from figlet. This is incredibly useful for seeing errors
immediately. Let's look at an example.

This is a normal syslog file:

    Jun 14 03:40:42 asdf[14063]: boring message
    Jun 14 03:40:43 asdf[14082]: boring message 2
    Jun 14 03:40:44 asdf[14102]: boring message 3
    Jun 14 03:40:45 asdf[14121]: boring message 4
    Jun 14 03:40:45 asdf[14159]: EVERYTHING IS BROKEN
    Jun 14 03:40:45 asdf[14140]: boring message 5
    Jun 14 03:40:46 asdf[14178]: boring message 6
    Jun 14 03:40:47 asdf[14197]: boring message 7
    Jun 14 03:40:48 asdf[14216]: boring message 8
    Jun 14 03:40:49 asdf[14235]: boring message 9

See how hard that was to notice in the middle of all those lines? It sure took
me a while to see it! Let's look at syslol's output of the same logs...

    Jun 14 03:40:42 asdf[14063]: boring message
    Jun 14 03:40:43 asdf[14082]: boring message 2
    Jun 14 03:40:44 asdf[14102]: boring message 3
    Jun 14 03:40:45 asdf[14121]: boring message 4
    Jun 14 03:40:45 asdf[14159]: EVERYTHING IS BROKEN
       ______  __      __  ______   _____   __     __  _______   _    _   _____   _   _    _____     _____    _____     ____    _____     ____    _  __  ______   _   _
      |  ____| \ \    / / |  ____| |  __ \  \ \   / / |__   __| | |  | | |_   _| | \ | |  / ____|   |_   _|  / ____|   |  _ \  |  __ \   / __ \  | |/ / |  ____| | \ | |
      | |__     \ \  / /  | |__    | |__) |  \ \_/ /     | |    | |__| |   | |   |  \| | | |  __      | |   | (___     | |_) | | |__) | | |  | | | ' /  | |__    |  \| |
      |  __|     \ \/ /   |  __|   |  _  /    \   /      | |    |  __  |   | |   | . ` | | | |_ |     | |    \___ \    |  _ <  |  _  /  | |  | | |  <   |  __|   | . ` |
      | |____     \  /    | |____  | | \ \     | |       | |    | |  | |  _| |_  | |\  | | |__| |    _| |_   ____) |   | |_) | | | \ \  | |__| | | . \  | |____  | |\  |
      |______|     \/     |______| |_|  \_\    |_|       |_|    |_|  |_| |_____| |_| \_|  \_____|   |_____| |_____/    |____/  |_|  \_\  \____/  |_|\_\ |______| |_| \_|



    Jun 14 03:40:45 asdf[14140]: boring message 5
    Jun 14 03:40:46 asdf[14178]: boring message 6
    Jun 14 03:40:47 asdf[14197]: boring message 7
    Jun 14 03:40:48 asdf[14216]: boring message 8
    Jun 14 03:40:49 asdf[14235]: boring message 9

I know which one **I** prefer. I saw the error immediately. I'm sure you'll
agree, this is much better.

syslol is clean and minimal - no config files, no mess. It comes in at exactly
one hundred lines of hand-crafted, beautiful Python code, so you can tweak it
to your needs. You'll be the life of the party if you use syslol.

Testing if syslol is for you is a snap. Simply run syslol.py, specifying the
port to listen on:

    $ syslol --port 1514

And in a separate terminal, send some syslol messages to it:

    $ logger -i --server 127.0.0.1 --udp -P 1514 "EVERYTHING IS BROKEN" -t asdf -p 0

That about sums it up. Try syslol today!
