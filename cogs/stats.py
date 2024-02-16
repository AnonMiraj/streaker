# import discord
# from discord.ext import commands
# from database import Stats
# from tabulate import tabulate
# from funks import checkisinstance
# import matplotlib.pyplot as plt
#
#
# class stats(commands.Cog):  # create a class for our cog that inherits from commands.Cog
#     # this class is used to create a cog, which is a module that can be added to the bot
#
#     def __init__(
#         self, bot
#     ):  # this is a special method that is called when the cog is loaded
#         self.bot = bot
#
#     @discord.slash_command()
#     async def top(self, ctx: discord.ApplicationContext, amonut:int=10 ):
#
#
#         async with ctx.typing():
#             # Header for the table
#             headers = ["RANK", "MEMVER", "PROBLEMS", "STREAK","DAYS"]
#             stat10 = tabulate(Stats.top_ten(amonut), headers=headers, tablefmt="double_grid")
#
#             embed = discord.Embed(
#             title=f"leader boards",
#             color=discord.Colour.blurple(),
#             description=f"```{stat10}```",
#             )
#
#         await ctx.send(embed=embed)
#
#
#     @discord.slash_command()
#     async def graph(self, ctx: discord.ApplicationContext, amount: int = 10):
#         try:
#             if amount <= 0:
#                 await ctx.send("Please specify a positive number for the amount.")
#                 return
#
#             async with ctx.typing():
#                 # Create a bar chart
#                 _, ax = plt.subplots()
#
#                 top_trainees = Stats.top_ten(amount)
#
#                 # Extract data for plotting
#                 members = [row[1] for row in top_trainees]
#                 problems_solved = [row[2] for row in top_trainees]
#                 streaks = [row[3] for row in top_trainees]
#
#                 # Plotting streaks
#                 ax.bar(members, streaks, label='Streak', color='blue')
#
#                 # Plotting problems solved on the second y-axis
#                 ax2 = ax.twinx()
#                 ax2.plot(members, problems_solved, label='Problems Solved', color='green', marker='o')
#
#                 # Adding labels and title
#                 ax.set_xlabel('Trainee')
#                 ax.set_ylabel('Streak', color='blue')
#                 ax2.set_ylabel('Problems Solved', color='green')
#                 ax.set_title('Leaderboard')
#
#                 # Set appropriate axis limits
#                 ax.set_ylim(0, max(streaks) * 1.2)
#                 ax2.set_ylim(0, max(problems_solved) * 1.2)
#
#
#                 # Combine legends
#                 lines, labels = ax.get_legend_handles_labels()
#                 lines2, labels2 = ax2.get_legend_handles_labels()
#                 ax.legend(lines + lines2, labels + labels2, loc='upper right')
#
#
#                 plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
#
#                 plt.tight_layout()  # Adjust layout to prevent overlap
#                 # Save the plot
#                 plt.savefig('plot.png')
#                 # Close the plot to release resources
#                 plt.close()
#
#             # Send the file as an attachment
#             with open('plot.png', 'rb') as file:
#                 await ctx.send(file=discord.File(file, 'plot.png'))
#
#         except Exception as e:
#             await ctx.send(f"An error occurred: {e}")
#
#
#     @discord.slash_command()
#     async def stats(self, ctx: discord.ApplicationContext):
#         # Defer the response while fetching data to not timeout
#         await ctx.defer()
#
#         # Create an embed to display stats
#         embed = discord.Embed(
#             title=f"Streaker stats", color=discord.Colour.blurple()
#         )
#
#         # Fetch and add data for the top streaker
#         top_streaker = Stats.highest_streaker()
#         embed = checkisinstance(
#             embed=embed,
#             title="Top Streaker",
#             value_title="streaks",
#             obj=top_streaker,
#             objx=tuple,
#         )
#
#         embed.add_field(name="-", value="", inline=False)
#
#         # Fetch and add data for the highest current streaker
#         highest_current_streaker = Stats.highest_current_streaker()
#         embed = checkisinstance(
#             embed=embed,
#             title="Top current Streaker",
#             value_title="streaks",
#             obj=highest_current_streaker,
#             objx=tuple,
#         )
#
#         embed.add_field(name="-", value="", inline=False)
#
#         # Fetch and add data for the highest problems solver
#         highest_problems_solver = Stats.highest_problems_solver()
#         embed = checkisinstance(
#             embed=embed,
#             title="most problems sovled",
#             value_title="problems solved",
#             obj=highest_problems_solver,
#             objx=tuple,
#         )
#
#         # Set a footer with a competition invitation URL
#         embed.set_footer(text="compete with us on https://streaker.com (example url)")
#
#         # Send the embed as a response
#         await ctx.followup.send(embed=embed)
#
#
# def setup(bot):  # this is called by Pycord to setup the cog
#     bot.add_cog(stats(bot))  # add the cog to the bot
