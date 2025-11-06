from discord.ext.commands import Cog, command
import os.path, asyncio, tempfile
from asyncio.subprocess import PIPE, STDOUT
import cogs.admin

MINISCRIPT_EXEC = os.path.normpath(os.path.join(os.path.dirname(__file__),"..","miniscript"))

class MiniScriptCog(Cog, name="MiniScript"):
	def __init__(self,bot):
		self.bot=bot
	async def run(self, code):
		with tempfile.NamedTemporaryFile("w",delete_on_close=False) as tf:
			tf.write(code)
			tf.close()
			proc = await asyncio.create_subprocess_exec(MINISCRIPT_EXEC,tf.name,stdout=PIPE,stderr=STDOUT)
			try:
				stdout, stderr = await asyncio.wait_for(proc.communicate(),timeout=5.0)
				return stdout, proc.returncode
			except asyncio.TimeoutError:
				proc.kill()
				return "Command timed out.", None
	@command("exec",brief="Run MiniScript code.")
	async def exec_cmd(self,ctx,*,code):
		code = cogs.admin.AdminCog.cleanup_code(code)
		stdout, returncode = await self.run(code)
		if returncode is None:
			await ctx.send(stdout)
			return
		if stdout==b'': stdout=b'[THIS SPACE LEFT INTENTIONALLY BLANK]'
		msg = f"```\n{stdout.decode().expandtabs(8)}\n```"
		if returncode != 0:
			msg = f"MiniScript exited with return code {returncode!s}.\n"+msg
		await ctx.send(msg)

async def setup(bot):
	await bot.add_cog(MiniScriptCog(bot))

if __name__=="__main__": print(MINISCRIPT_EXEC)
