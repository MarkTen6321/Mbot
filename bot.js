//Modules
console.log("Starting Bot....");
var Discord = require('./woorv6.js'); //Discord
var gis = require('g-i-s'); //Google Image Search
var oneLinerJoke = require('one-liner-joke'); //Joke
const urban = require('urban.js'); //Dictionary
var weather = require('weather-js'); //Weather
var h2p = require('html2plaintext') //HTML to Plain Text
var google = require('google'); //Google Search
const lib = require('thoughts'); //Random Thoughts
var tarot = require('./tarot')//tarot

//RSS
let Parser = require('rss-parser');
let parser = new Parser();

var giphy = require('giphy-api')(process.env.GIF);
var atr1 = "https://cdn.discordapp.com/attachments/429134650288635906"
var atr2 = "/437623169294008331/Poweredby_100px_Badge.gif" //LOL SidSoy

//Discord Initilization
var bot = new Discord.Client({
    token: process.env.DIS,
    autorun: true
})
bot.on('ready', function () {
    console.log();
    console.info('Connecting Bot....');
    console.info(bot.username + ' - (' + bot.id + ')');
});
bot.setPresence({
    game: {
        name: "UNDER Trials"
    }
});


//Commands 
let fcommands =`
MHug (@Person)         : Hug Someone
Mcudle (@Person)       : Cuddle with Someone
Mkiss (@Person)        : Kiss Someone
Mpat (@Person)         : Pat Someone
Mkick (@Person)        : Kick Someone
Mslap (@Person)        : Slap Someone
Mpoke (@Person)        : Poke Someone
Mhigh5 (@Person)       : Give Someone a High Five
Mthrow (@Person)       : Throw something at Someone
Mjoke                  : Random Joke
Mthought               : Shows a Random  Thought
MSthought              : Shows a Shower Thought
Mtarot                 : Lets do some tarot reading
Manon (Message)        : Post Anything Anonymously
Mdice                  : Throw a Dice
Mflip                  : It doesn't Flip but Flips a Coin
Myesno (Question)      : Says Yes or No to a Question
Mor (Option 1 or 2)    : Chooses between two options
Mgift (@Person) (Gift) : Gift Something to someone`

let ucommands =`
Mword (Word)           : Get Definiton of a Word
Mgoogle (Search Query) : Get Google Search Results
Mgif (Search Query)    : Search GIFs
Mimage (Search Query)  : Search Images
Mpost (#channel)       : Post something in a Nice Text Box
Mpoll (#chl) (Reaction 1 and 2): Do some cool Polls in a snap
Mwea (Place)           : Get Weather Info
Mnews                  : Get Latest News`

let mcommands = `
Manounce <#channel>      : Announce something
Mrole <@Person> <(Role)> : Add someone to a Role in a snap
Munrole <@Person> <(Role)> : Remove someone from a Role
Mmute <@Person>          : Mute Someone
Munmute <@Person>        : Unmute Someone`


//
var ban

//Colors
var pink = 14684241
var purple = 9442302
var red = 15147864
var green = 4772641
var blue = 32479
//functions
function sendEmbeds(a, b, c) {
    bot.sendMessage({
        to: a,
        embed: {
            color: b,
            description: "**" + c + "**",
        }
    })
}
function report(report) {
    bot.sendMessage({
        to: "332555437234978828",
        message: "```" + report.statusMessage + "```"
    })
}

//Message Event Happens
bot.on('message', function (user, userID, channelID, message, event) {
    //Necessary Variables
    let messaget
    let serverID = event.d.guild_id
    function nick() {
        var nick = bot.servers[serverID].members[userID].nick || user
        return nick
    }

    function errorm(err) {
        sendEmbeds(channelID, blue, "Somethings Wrong Report sent to Developer")
        report(err)
    }

    let r = message.split(" ")
    r.splice(0, 2)
    let reason = r.join(" ")

    function persmissions() {
        //Permissions
        let userHasPermission
        let serverID = event.d.guild_id
        let rolesOfUser = bot.servers[serverID].members[userID].roles
        let rolesInServer = bot.servers[serverID].roles
        for (let roleIndex in rolesOfUser) {
            if (userHasPermission) break
            if (rolesInServer[rolesOfUser[roleIndex]]['GENERAL_ADMINISTRATOR']) userHasPermission = true
        }
        return userHasPermission
    }

    function nick2() {
        let nick2 = bot.servers[serverID].members[event.d.mentions[0].id].nick || event.d.mentions[0].username
        return nick2
    }

    function extract() {
        a = message.substring(message.indexOf("<#") + 2, message.indexOf(">"))
        return a;
    }
    let matter = message.substring(6)
    //Necessary Array of Messages
    var args = message.toLowerCase().substring(1).split(' ')
    //Nexessary functions
    function GIF(q, to) {
        giphy.search({
            q: q,
            rating: 'g'
        }, function (err, res) {
            let x = Math.floor(Math.random() * res.data.length)
            let t = ("https://media.giphy.com/media/" + res.data[x].id + "/giphy.gif");
            bot.sendMessage({
                to: to,
                embed: {
                    color: purple,
                    footer: {
                        icon_url: atr1 + atr2,
                        text: "Powered by GIPHY"
                    },
                    image: {
                        url: t
                    }
                }
            })
        });
    }

    function image(error, results) {
        if (error) {
            console.log(error);
        }
        else {
            let x = Math.floor(Math.random() * 10)
            let img = results[x].url
            bot.sendMessage({
                to: channelID,
                embed: {
                    color: purple,
                    image: {
                        url: img
                    }
                }
            })
        }
    }

        if (message.toLowerCase().substring(0, 1) === "m") {
        if (args[0] === "hug") {
            console.log(`Hug asked by ${user}`)
            GIF("Bro Hug", channelID);
            !args[1] ? messaget = `${nick()} is sharing some LOVE !!!` :
                nick() === nick2() ? messaget = `Mbot gave you a hug, ${nick()}` :
                    messaget = `Oooooooooooh! ${nick()} gave a tight hug to ${nick2()}`;

            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "cudle") {
            console.log(`Cuddle asked by ${user}`)
            GIF("Cuddle", channelID);
            !args[1] ? messaget = `${nick()} is sharing Loads of LOVE !!!` :
                nick() === nick2() ? messaget = `Will you cuddle with me ?, ${nick()}` :
                    messaget = `Oooooooooooh! ${nick()} cuddled with ${nick2()}`;
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "kiss") {
            console.log(`Kiss asked by ${user}`)
            GIF("Cheek Kiss", channelID);
            !args[1] ? messaget = `${nick()} Whom are you kissing ???` :
                nick() === nick2 ? messaget = `I am always there for you, ${nick()}` :
                    messaget = `${nick()} kissed ${nick2()} :kissing_closed_eyes:`

            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "pat") {
            console.log(`Pat-Pat asked by ${user}`)
            GIF("Patting", channelID);
            !args[1] ? messaget = `${nick()} Whom are you patting ???` :
                nick() === nick2() ? messaget = `Good self encouragement is Nice, ${nick()}` :
                    messaget = `${nick()} patted ${nick2()} :grin: `
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "kick") {
            console.log(`Kicked by ${user}`)
            GIF("kicking", channelID);
            !args[1] ? messaget = `${nick()} Whom are you kicking ??? LOL` :
                nick() === nick2() ? messaget = `What happend ?, ${nick()}` :
                    messaget = `${nick()} kicked ${nick2()} :rofl: `
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "slap") {
            console.log(`Slaped by ${user}`)
            GIF("bitch slap", channelID);
            !args[1] ? messaget = `${nick()} Oh are you trying kill some flies ???` :
                nick() === nick2() ? messaget = `Any Explanation ? ${nick()}` :
                    messaget = `${nick()} slaped ${nick2()} :joy_cat: `
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "high5") {
            console.log(`${user} gave a high5`)
            GIF("high five", channelID);
            !args[1] ? messaget = `${nick()}, Can you give a High5 to me ? :yum: ` :
                nick() === nick2() ? messaget = `High5 !!! Mbot loves High5s` :
                    messaget = `Yay !!! :sunglasses: ${nick()} gave a high5 to ${nick2()}`
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "dance") {
            console.log(`${user} is dancing LOL`)
            GIF("Dancing", channelID);
            !args[1] ? messaget = `${nick()}, Turn up the music ! :speaker:` :
                nick() === nick2() ? messaget = `Lets Nacho(Dance) !!! :dancers:` :
                    messaget = `${nick2()}, Hey Come lets Dance together !!! :man_dancing: :dancer:`
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "poke") {
            console.log(`${user} poked`)
            GIF("poking", channelID);
            !args[1] ? messaget = `${nick()}, I am always here !` :
                nick() === nick2() ? messaget = `I know Boredom hits HARD sometimes :rolling_eyes:` :
                    messaget = `${nick2()}, Heyu ${nick()} is poking you !!! :grin:`
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }
        else if (args[0] === "meh") {
            console.log(`${user} is like "Meh"`)
            GIF("meh", channelID);
            !args[1] ? messaget = `${nick()}, Lets go Meh...................` :
                nick() === nick2() ? messaget = `Meh....Try some other commands` :
                    messaget = `${nick2()}, Hey ${nick()} is bored AF`
            setTimeout(() => { sendEmbeds(channelID, pink, messaget) }, 500)
        }

        else if (args[0] === "dice") {
            let d = (Math.floor(Math.random() * 5)) + 1;
            sendEmbeds(channelID, pink, `${nick()}, Ooooooooooooooooh It is a ${d} :game_die:`)
        }
        else if (args[0] === "yesno") {
            let ans = ["Yes", "Absolutely", "Ofcourse", "No", "Am not sure", "Maybe"]
            let x = ans[Math.floor(Math.random() * ans.length)]
            let ans2 = `Question:** ${message.substring(7)} **Answer: ${x}`
            sendEmbeds(channelID, pink, ans2)
            setTimeout(() => { GIF(x, channelID) }, 500)
        }
        else if (args[0] === "gift") {
            let m = message.split(" ")
            let s
            if (args[2]) {
                m.splice(0, 2)
                s = m.join(" ")
            }
            else {
                m.splice(0, 1)
                s = m.join(" ")
            }
            let m2;
            event.d.mentions ?
                m2 = `${nick()} gave ${nick2()} ${s} :hearts:` : m2 = `A ${s} for ???? :smirk:`
            sendEmbeds(channelID, pink, m2)
            setTimeout(() => { gis(s, image) }, 500)
        }
        else if (args[0] === "flip") {
            let f = Math.floor(Math.random)
            let s
            f ? s = "Its.......... Heads :white_circle:" : s = "Its........... Tails :white_circle: "
            sendEmbeds(channelID, pink, s)
            setTimeout(() => { GIF("Coin Flip", channelID) }, 500);
        }
        else if (args[0] === "throw") {
            let things2 = ["Bottle", "Garbage", "Football", "Banana Peel", "Fish", "Water"]
            let b = things2[Math.floor(Math.random() * things2.length)]
            let mes
            args[1] ? mes = `${nick()}, Threw ${b} on ${nick2()} :rofl:` :
                mes = `${nick()} threw ${b} on Someone :grin:`
            sendEmbeds(channelID, purple, mes)
        }
        else if (args[0] === "joke") {
            let getRandomJoke = oneLinerJoke.getRandomJoke();
            sendEmbeds(channelID, purple, getRandomJoke.body)
            setTimeout(() => { GIF("lmao", channelID) }, 400)
        }
        else if (args[0] === "thought") {
            let random = lib.random();
            let anotherRandom = lib.random("anonymous");
            let particular = lib.particular("anonymous", 2);
            sendEmbeds(channelID, pink, "Thought : :bouquet: :confetti_ball: :beers:")
            setTimeout(() => { sendEmbeds(channelID, purple, random.thought) }, 500)
            setTimeout(() => { GIF("hmmm", channelID) }, 400)
        }
        else if (args[0] === "image") {
            let q = message.substring(7)
            var m = event.d.id
            var c = channelID
            sendEmbeds(channelID, pink, "Your Search Result: :mag:")
            setTimeout(() => { gis(q, image) }, 500)
        }
        else if (args[0] === "google") {
            let art1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/"
            let art2 = `5/53/Google_"G"_Logo.svg/1000px-Google_"G"_Logo.svg.png`
            let art3 = art1 + art2
            let query = message.toLowerCase().substring(8)
            google.resultsPerPage = 3;
            google(query, function (err, res) {
                if (err) {
                    console.log(err)
                    sendEmbeds(channelID, red, "ERROR")
                }
                else {
                    gis(query, image)
                    bot.sendMessage({
                        to: channelID,
                        embed: {
                            title: "Search Results: ",
                            color: 4772641,
                            author: {
                                name: "Google",
                                icon_url: art3
                            },
                            fields: [
                                {
                                    name: "1." + (res.links[0].title || "No Title") + ": ",
                                    value: (res.links[0].link || "No Link") + "\n" + res.links[0].description || "No Description"
                                },
                                {
                                    name: "2." + (res.links[1].title || "No Title") + ": ",
                                    value: (res.links[0].link || "No Link") + "\n" + res.links[1].description || "No Description"
                                },
                                {
                                    name: "3." + (res.links[2].title || "No Title") + ": ",
                                    value: (res.links[0].link || "No Link") + "\n" + res.links[2].description || "No Description"
                                }
                            ]
                        }
                    });
                }
            });
        }
        else if (args[0] === "gif") {
            sendEmbeds(channelID, pink, "Your GIF Result: ")
            setTimeout(() => { GIF(message.substring(5), channelID) }, 400)
        }
        else if (args[0] === "word") {
            let art1 = "http://www.amtrending.com/wp-content"
            let art2 = "/uploads/2016/08/urban-dictionary-cover.jpg"
            let art3 = art1 + art2
            urban(message.substring(6)).then(function (res) {
                bot.sendMessage({
                    to: channelID,
                    color: purple,
                    embed: {
                        title: "Word: " + res.word,
                        color: purple,
                        author: {
                            name: "Urban Dictionary",
                            icon_url: art3
                        },
                        fields: [
                            {
                                name: "Definition:",
                                value: res.definition.substring(0, 1000) + ".............."
                            },
                            {
                                name: "Example:",
                                value: res.example
                            }
                        ]
                    }
                });
            });
        }
        else if (args[0] === "tarot") {
            var l = Math.floor(Math.random() * 23)
            var s = Math.floor(Math.random() * 2)
            var t = Object.values(tarot);
            console.log(t[l]);
            if (s <= 1) {
                var h = t[l].about0
            }
            else {
                var h = t[l].about1
            }
            bot.sendMessage({
                to: channelID,
                embed: {
                    color: purple,
                    image: {
                        url: t[l].link0
                    }
                }
            })
            sendEmbeds(channelID, pink, "The card says about: " + h)
        }
        else if (args[0] === "nick") {
            console.log(reason)
            bot.editNickname({
                serverID: event.d.guild_id,
                userID: event.d.mentions[0].id,
                nick: reason
            }, function (err, res) {
                if (err) { 
                    errorm(err)
                    console.log(err) }
                else {
                    sendEmbeds(channelID, pink, "Nickname set to: " + reason)
                }
            });
        }
        else if (args[0] === "post") {
            sendEmbeds(extract(), pink, nick() + " says: " + reason)
        }
        else if (args[0] === "sthoughts") {
            (async () => {
                let feed = await parser.parseURL('https://www.reddit.com/r/Showerthoughts/.rss');
                let n = Math.floor(Math.random() * feed.items.length)
                if (n === 1) n + 2
                else if (n === 0) n + 3
                sendEmbeds(channelID, pink, "Shower Thought :")
                setTimeout(() => { sendEmbeds(channelID, purple, feed.items[n].title) }, 400)
            })();
        }
        else if (args[0] === "poll") {
            let k = args[2];
            let j = args[3];
            bot.sendMessage({
                to: extract(args[1]),
                message: args.slice(4).join(' ')
            }, function (err, res) {

                setTimeout(() => {
                    bot.addReaction({
                        channelID: res.channel_id,
                        messageID: res.id,
                        reaction: k
                    })
                }, 400)

                setTimeout(() => {
                    bot.addReaction({
                        channelID: res.channel_id,
                        messageID: res.id,
                        reaction: j
                    })
                }, 800)
            })
        }
        else if (args[0] === "news") {
            (async () => {
                let feed = await parser.parseURL('http://rss.cnn.com/rss/edition_world.rss');
                let n = Math.floor(Math.random() * feed.items.length)
                bot.sendMessage({
                    to: channelID,
                    embed: {
                        color: purple,
                        title: feed.items[n].title,
                        description: h2p(feed.items[n].content) + "\n\nRead More at: " + feed.items[n].link ,
                        footer: {
                            text: "From CNN News"
                        }
                    }
                })
            })();
        }
        else if (args[0] === "wea") {
            weather.find({ search: message.substring(4), degreeType: 'C' }, function (err, result) {
                if (err) console.log(err);
                let location = result[0].location.name
                let temperature = result[0].current.temperature + " Celsius"
                let skytext = result[0].current.skytext
                let humidity = result[0].current.humidity + " Percentage"
                let winddisplay = result[0].current.winddisplay
                bot.sendMessage({
                    to: channelID,
                    embed: {
                        color: pink,
                        title: "Weather :",
                        fields: [
                            {
                                name: "Location :",
                                value: location
                            },
                            {
                                name: "Temperature :",
                                value: temperature
                            },
                            {
                                name: "Sky Text :",
                                value: skytext
                            },
                            {
                                name: "Humidity :",
                                value: humidity
                            },
                            {
                                name: "Wind :",
                                value: winddisplay
                            }
                        ]
                    }
                })

            });
        }

        //Admin Commands
        else if (args[0] === "anoun") {
            if (persmissions()) {
                bot.sendMessage({ to: channelID, message: "@everyone" })
                sendEmbeds(channelID, purple, "Announcement: \n" + reason)
            }
            else (
                sendEmbeds(channelID, red, "Are you the Admin or trying to be one ?")
            )
        }
        else if (args[0] === "role") {
            if (persmissions()) {
                let rol = message.substring(message.indexOf("(") + 1, message.indexOf(")"))
                let roles = bot.servers[serverID].roles;
                let roleID = Object.keys(roles).find(r => roles[r].name === rol);
                bot.addToRole({
                    serverID: event.d.guild_id,
                    userID: event.d.mentions[0].id,
                    roleID: roleID
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else {
                        sendEmbeds(channelID, red, `Done ${event.d.mentions[0].username} added to ${rol}`)
                    }
                });
            }
            else { sendEmbeds(channelID, red, "You dont have permissions !") }
        }
        else if (args[0] === "unrole") {
            if (persmissions()) {
                let rol = message.substring(message.indexOf("(") + 1, message.indexOf(")"))
                let roles = bot.servers[serverID].roles;
                let roleID = Object.keys(roles).find(r => roles[r].name === rol);
                bot.removeFromRole({
                    serverID: event.d.guild_id,
                    userID: event.d.mentions[0].id,
                    roleID: roleID
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else {
                        sendEmbeds(channelID, red, `Done ${event.d.mentions[0].username} removed from ${rol}`)
                    }
                });
            }
            else { sendEmbeds(channelID, red, "You dont have permissions !") }
        }
        else if (args[0] === "ban") {
            let mes = message.split(" ")
            mes.splice(0, 2)
            mes = mes.join(" ")
            if (persmissions()) {
                bot.ban({
                    serverID: event.d.guild_id, userID: event.d.mentions[0].id
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else {
                        sendEmbeds(channelID, red, `You have succesfully banned ${event.d.mentions[0].username}. Reason: ${reason}`)
                        sendEmbeds(channelID, pink, "Note: Unban can be done only manually")
                    }
                });

            }
            else { sendEmbeds(channelID, red, "You dont have permissions !!!") }
        }
        else if (args[0] === "mute") {
            if (persmissions()) {
                bot.mute({
                    serverID: event.d.guild_id,
                    userID: event.d.mentions[0].id
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else {
                        sendEmbeds(channelID, pink, `You have muted ${event.d.mentions[0].username}. Reason: ${reason}`)
                        sendEmbeds(channelID, green, "Use unmute <person> to Unmute")
                    }
                });
            }
            else { sendEmbeds(channelID, red, "You dont have permissions !!!") }
        }
        else if (args[0] === "unmute") {
            if (persmissions()) {
                bot.unmute({
                    serverID: event.d.guild_id,
                    userID: event.d.mentions[0].id
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else {
                        sendEmbeds(channelID, blue, "Unmuted")
                    }
                });
            }
            else { sendEmbeds(channelID, red, "You dont have permissions !!!") }
        }
        else if (args[0] === "akick") {
            if (persmissions()) {
                bot.kick({
                    serverID: event.d.guild_id,
                    userID: event.d.mentions[0].id
                }, function (err, res) {
                    if (err) { errorm(err) }
                    else { sendEmbeds(channelID, red, `${event.d.mentions[0].username} was kicked. Reason: ${reason}`) }
                })
            }
            else { sendEmbeds(channelID, red, "You dont have permissions !!!") }
        }
        else if (args[0] === "tes") {
            console.log(event.d.guild_id)
            bot.getBans(event.d.guild_id, function (err, res) {
                console.log(res)
            })
        }
        else if (args[0] === "commands") {
            sendEmbeds(channelID, pink, "Commands :")
            setTimeout(() => {
                bot.sendMessage({
                    to: channelID,
                    embed: {
                        title: "Commands of MBot:",
                        color: red,
                        fields: [
                            {
                                name: "Fun Commands:",
                                value: "```" + fcommands + "```"
                            },
                            {
                                name: "Utility Commands:",
                                value: "```" + ucommands + "```"
                            },
                            {
                                name: "Admin Commands:",
                                value: "```" + mcommands + "```"
                            }
                        ]
                    }
                })
            }, 200)
        }
    }
})

bot.on("disconnect", (err, code) => console.log(err, code));
