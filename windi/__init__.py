from subprocess import Popen

# Start an indi server
#
# @param serverType {String} - type of server to run. e.g. "v4l2 ccd" -> "indi_v4l2_ccd"
def startServer(serverType):
    serverType = 'indi_' + serverType.replace(' ', '_').lower()
    Popen(['bash', './bash/server.sh', serverType])


# Kill the server started in start server function (or in the command line)
#
# @param port {number} - port of server to terminate. default value is 7624.
def killServer(port=7624):
    Popen(['bash', './bash/kill.sh', str(port)])
