# RobinhoodBot
Trading bot for Robinhood accounts.

Don't be stupid. Investing with bots can be risky. Use this software only at your own risk.

This bot is a work in progress. My goal is to try out a new trading algorithm which I have in my head.

## What am I trading?

This bot is to take a currency pair (like DOGE:USD, for example), and convert the volatility into profit.

In this program, I choose to focus on trading cryptocurrencies mainly because cryptos lack an underlying concept of value in the same way that stocks do. For example, cryptocurrencies are not shares of a company. They have no boards of directors (although you might consider the miners/validators of a given blockchain network to be a form of "board of directors") and no sales (although the crypto assets themselves are increasingly used as a means of conducting sales). Instead, cryptocurrencies are, well, ...currencies. This means that any arbitrary price is basically just as valid as any other possible price, since cryptocurrencies lack many of the traditional measurements of an asset's worth. This makes it no surprise that cryptocurrencies tend to be extremely volatile as an asset class. Since my algorithm is targeting volatile assets, cryptocurrencies are a natural fit.

Another benefit of starting with cryptocurrencies is that the trading hours never end. With stock exchanges, there are business hours during which all (or most) stock trading must happen. However, public blockchain networks never sleep. This means that my algorithm can work 24 hours a day, 7 days a week. Since I have confidence in my strategy, this means that cryptocurrencies offer me even more opportunity for gains.

## Why Robinhood?

Robinhood shields me from the transaction fees of crypto transactions. Since I plan for my bot to do a lot of transactions, all those fees would likely threaten my profits if I were trading crypto at an exchange. Obviously, having zero fees to trade is a huge incentive. However, one downside to using Robinhood is that I do not actually control the keys to my crypto, but instead need to trust Robinhood as a third-party steward of my keys. Nonetheless, I consider the tradeoff to be worth it. I will want to be on the lookout for ways to cut out the need for a third-party, but first things first: I need to test that my concept even works, and only then figure out how to make it decentralized, anonymous, etc.

This is my MVP (minimum viable product) after all! It's not going to be perfect the first time. But it will hopefully get better with each iteration. If you are an open source developer who would like to collaborate on this, please let me know, and please forgive me in advance for any ignorance I might have of dev customs/best-practices. I started learning to code last year. LOL.  

## What do I need to do to get started:

Install pip on the machine you plan to use as this bot's home.

<code>sudo apt install python3-pip</code>

<code>sudo pip3 install robin_stocks</code>
<code>sudo pip3 install pandas</code>
<code>sudo pip3 install ta</code>
I also need to upgrade my version of numpy, since it is outdated:
<code>sudo pip3 install numpy --upgrade</code>
<code>sudo pip3 install matplotlib</code>
## For more info:
Jonathan A. McCormick, Jr.
Email mccormick9 (at) protonmail (dot) com.
