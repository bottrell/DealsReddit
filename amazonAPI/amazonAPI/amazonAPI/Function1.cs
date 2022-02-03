using System;
using System.Collections.Generic;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
//https://html-agility-pack.net/
using HtmlAgilityPack;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net;

namespace amazonAPI
{
    public class Function1
    {
        [FunctionName("Function1")]
        public async Task Run([TimerTrigger("0 0 8 * * *",
        #if DEBUG
            RunOnStartup= true
        #endif
            )]TimerInfo myTimer, ILogger log)
        {
            //Body 
            //Goal is to populate our cosmos DB with all the items in the "Today's deals" page https://www.amazon.com/deals?ref_=nav_cs_gb
            //Only add something to the cosmos DB if the discount is greater than 50%
            string baseURL = "https://www.amazon.com/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%25228843C6381E792DA8FAE9FC70756AAFF2%2522%252C%2522discountRanges%2522%253A%255B%257B%2522from%2522%253A10%252C%2522to%2522%253A25%252C%2522selected%2522%253Afalse%257D%252C%257B%2522from%2522%253A25%252C%2522to%2522%253A50%252C%2522selected%2522%253Afalse%257D%252C%257B%2522from%2522%253A50%252C%2522to%2522%253A70%252C%2522selected%2522%253Atrue%257D%252C%257B%2522from%2522%253A70%252C%2522to%2522%253A100%252C%2522selected%2522%253Afalse%257D%255D%252C%2522dealType%2522%253A%2522LIGHTNING_DEAL%2522%252C%2522sorting%2522%253A%2522BY_DISCOUNT_DESCENDING%2522%257D";
            string shortURL = "https://www.amazon.com/";
            

            log.LogInformation($"C# Timer trigger function execute - looking for top 10 deals at {shortURL}");

            //getting the html
            var html = await GetHTML(shortURL);

            //getting a list of links for top 10 discounted items
            top10discounts(html, log);

        }

        //requires : html corresponds to valid html 
        //modifies : nothing
        //returns : a list of links that correspond to the top 10 discounted items at that time
        public List<string> top10discounts (string html, ILogger log)
        {
            
            var htmlDoc = new HtmlDocument();
            htmlDoc.LoadHtml(html);

            //log.LogInformation($"{html}");

            // all the links should exist within Deals Grid
            //div aria-label="Deals Grid"
            var apage = htmlDoc.DocumentNode.SelectNodes("//div[@id='a-page']");
            htmlDoc.LoadHtml(apage[0].InnerHtml);
            //log.LogInformation(htmlDoc.Text);
            var allslots = htmlDoc.DocumentNode.SelectNodes("//a[@class='a-link-normal']");
            log.LogInformation(allslots[1].InnerText);

            // all the links should start with <div class="a-link-normal"

            List<string> links = new List<string>();
            return links;
        }

        //requires : url is a valid string
        //modifies : nothing
        //returns : a string corresponding to the html that exists at url
        public Task<string> GetHTML(string url)
        {
            //amazon.com is encrypted, so we need to decompress
            HttpClientHandler handler = new HttpClientHandler()
            {
                AutomaticDecompression = System.Net.DecompressionMethods.GZip | DecompressionMethods.Deflate
            };

            //load the html from the page
            var client = new HttpClient(handler);
            return client.GetStringAsync(url);
        }

    }
}
