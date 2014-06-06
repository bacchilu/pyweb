# PyWeb

Usefull if you need to add an HTTP command parser to your python script. HTTP requests are passed to a controller to be processed.

You can use the framework in this way:

    import commander
    

    def dummyFn(host, path):
        pass
    
    
    commander.start(dummyFn)

The _command_ module implements a cmd shell where you can send some commands to the application. The _start_ function starts the shell. You must pass a function to the commander, that function will be executed in response to each HTTP request.

When you start the _commander_, you are promt a command shell with the following commands available:

    (Cmd) help

    Documented commands (type help <topic>):
    ========================================
    exit  help  restart  start  status  stop

The _start_ command creates two new processed: the web and the controller. You can also use _start web_ or _start controller_.

Same considerations for the _stop_ command and the _status_ command.