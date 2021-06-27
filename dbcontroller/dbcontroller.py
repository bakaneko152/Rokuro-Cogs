import asyncio
import functools
import logging
from typing import Any, List, Optional, Tuple, Callable
import aiomysql

import discord

from redbot import VersionInfo, version_info
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n




_ = Translator("DBController", __file__)

log = logging.getLogger("red.rokuro-cogs.DBController")
default_global = {
    "storage_details": {
        "host": "localhost",
        "port": 3306,
        "user": "user",
        "password": "pass",
        "db": "db",
        "charset": "utf8mb4"
    },
}
@cog_i18n(_)
class DBController(commands.Cog):
    """
    Cog for Save
    """

    __author__ = ["bakaneko"]
    __version__ = "1.0.1"
    #https://github.com/Acronexp/AwsmCogs/blob/main/bet/bet.py
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 4672942129256070, force_registration=True)

        self.config.register_global(**default_global)
        self.loop = asyncio.get_event_loop()
        self._pool = None#await aiomysql.create_pool(**storage_details, connect_timeout=5)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    async def initialize(self):
        settings = await self.config.storage_details.all()
        self._pool = await aiomysql.create_pool(**settings, connect_timeout=5)

    def cog_unload(self):
        log.debug("Unloading DBController...")
        if self._pool is not None:
            # await cls._pool.close()
            self._pool.close()
            await self._pool.wait_closed()
            log.debug("mysql disconnected.")
        log.debug("DBController unloaded.")
        
    @commands.group()
    @commands.is_owner()
    async def setmysql(self,ctx):
        """
        MySQL database settings
        """
        pass
    

    @setmysql.command()
    @checks.is_owner()
    async def host(self, ctx, db_host: str):
        """
        Sets the MySQL host, defaults to localhost (127.0.0.1)
        """
        try:
            await self.config.storage_details.host.set(db_host)
            await ctx.send(f"Database host set to: `{db_host}`")
        except (ValueError, KeyError, AttributeError):
            await ctx.send("There was an error setting the database's ip/hostname. Please check your entry and try again!")

    @setmysql.command()
    @checks.is_owner()
    async def port(self, ctx, db_port: int):
        """
        Sets the MySQL port, defaults to 3306
        """
        try:
            if 1024 <= db_port <= 65535:  # We don't want to allow reserved ports to be set
                await self.config.storage_details.port.set(db_port)
                await ctx.send(f"Database port set to: `{db_port}`")
            else:
                await ctx.send(f"{db_port} is not a valid port!")
        except (ValueError, KeyError, AttributeError):
            await ctx.send(
                "There was a problem setting your port. Please check to ensure you're attempting to use a port from 1024 to 65535")

    @setmysql.command(aliases=['name', 'user'])
    @checks.is_owner()
    async def username(self, ctx, user: str):
        """
        Sets the user that will be used with the MySQL database. Defaults to SS13
        It's recommended to ensure that this user cannot write to the database
        """
        try:
            await self.config.storage_details.user.set(user)
            await ctx.send(f"User set to: `{user}`")
        except (ValueError, KeyError, AttributeError):
            await ctx.send("There was a problem setting the username for your database.")

    @setmysql.command()
    @checks.is_owner()
    async def password(self, ctx, passwd: str):
        """
        Sets the password for connecting to the database
        This will be stored locally, it is recommended to ensure that your user cannot write to the database
        """
        try:
            await self.config.storage_details.password.set(passwd)
            await ctx.send("Your password has been set.")
            try:
                await ctx.message.delete()
            except(discord.DiscordException):
                await ctx.send("I do not have the required permissions to delete messages, please remove/edit the password manually.")
        except (ValueError, KeyError, AttributeError):
            await ctx.send("There was a problem setting the password for your database.")

    @setmysql.command(aliases=["db"])
    @checks.is_owner()
    async def database(self, ctx, db: str):
        """
        Sets the database to login to, defaults to feedback
        """
        try:
            await self.config.storage_details.db.set(db)
            await ctx.send(f"Database set to: `{db}`")
        except (ValueError, KeyError, AttributeError):
            await ctx.send("There was a problem setting your notes database.")

    @setmysql.command()
    @checks.is_owner()
    async def info(self, ctx):
        """
        Gets the current settings for the notes database
        """
        settings = await self.config.storage_details.all()
        embed = discord.Embed(title="__Current settings:__")
        for k, v in settings.items():
            if k != "admin_ckey":
                if k != "password":  # Ensures that the database password is not sent
                    if v == "":
                        v = None
                    embed.add_field(name=f"{k}:", value=v, inline=False)
                else:
                    embed.add_field(name=f"{k}:", value="`DATA EXPUNGED`", inline=False)
        await ctx.send(embed=embed)
    
    @setmysql.command()
    @checks.is_owner()
    async def reload(self, ctx):
        """
        Reload MySQL Settings and reconnection
        """
        if self._pool is not None:
            # await cls._pool.close()
            self._pool.close()
            await self._pool.wait_closed()
            await ctx.send("Connection Close.")
            settings = await self.config.storage_details.all()
            self._pool = await aiomysql.create_pool(**settings, connect_timeout=5)
            await ctx.send("reconnection.")
        

            
    async def execute(self, query: str, *args, method: Optional[Callable] = None) -> Any:
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                # if method is None:
                #     method = cur.execute#cls._pool.execute
                log.debug("Query: %s", query)
                if args:
                    log.debug("Args: %s", args)
                await cur.execute(query,*args)
                if method is None:
                    return
                elif method=="fetchone":
                    return await cur.fetchone()
                elif method=="fetchall":
                    return await cur.fetchall()
                elif method=="set":
                    await conn.commit()
                    return 1
    async def commit(self) -> Any:
        async with self._pool.acquire() as conn:
                await conn.commit()
                return 1

