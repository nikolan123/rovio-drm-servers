from flask import Flask, request

app = Flask(__name__)

# @app.route('/install/pc/update/AngryBirdsRio', methods=['GET'])
# def updatebirds7():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Rio
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=2.3.2
#     """

# @app.route("/install/pc/update/AngryBirds", methods=["GET"])
# def updatebirds6():
#     return f""";aiu;

# [Update]
# Name=Angry Birds
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/install/pc/update/AngryBirdsSeasonsFull", methods=["GET"])
# def updatebirds5():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Seasons Full
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/install/pc/update/AngryBirdsSpace", methods=["GET"])
# def updatebirds4():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Space
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/install/pc/update/AngryBirdsStarWars", methods=["GET"])
# def updatebirds3():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Star Wars
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/install/pc/update/AngryBirdsStarWarsII", methods=["GET"])
# def updatebirds2():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Star Wars II
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/install/pc/update/BadPiggies", methods=["GET"])
# def updatebirds1():
#     return f""";aiu;

# [Update]
# Name=Bad Piggies
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

# @app.route("/versionCheck/1/AngryBirdsClassic", methods=["GET"]) # replace the /versioncheck url with /install/pc/update/AngryBirds for version classic 2.3.0 and above
# def updatebirds8():
#     return f""";aiu;

# [Update]
# Name=Angry Birds Classic
# URL=http://yourip/yourfilename
# Size=yourfilesize
# MD5=yourfilemd5
# ServerFileName=yourfilename
# FilePath=[APPDIR]yourfilename
# Version=4.5.5
#     """

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
