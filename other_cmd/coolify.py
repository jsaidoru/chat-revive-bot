from discord.ext import commands
@commands.command()
async def coolify(ctx):
    await ctx.send("""
**COOLIFY MANUAL**
0. If you haven't done, create a GitHub repo:
 * Go to https://github.com/new
 * Make it public and don't initialize with README.md
 * Press **Create Repository**
 * After that, go back to coolify.
1. Go to **Projects**: https://coolify.artyom.me/projects. Add a new project, have a name (and description)
2. At the Resource tab, choose **New**
3. Choose your kind of application, often **Public Repository**
4. Enter the link of your GitHub repo (https:\//github.com/<your username>/<repository name>), press **Check Repository**, and if you are lazy, just pick the default settings
5. Press **Continue** and **Deploy** and your app will run forever.

There are some stuff you wanna know about too:
- Environment Variables: Store secrets for your project. Can be accessed through os.environ.get (for Python)
- Storage: A storage. Can be accessed through TinyDB("/storage/cooldowns.json")""")