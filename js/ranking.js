var rule = {
    类型: '影视',
    title: '📊 豆瓣榜单',
    host: 'https://raw.githubusercontent.com/yangclaw2026-png/tvbox-home/main/data',
    
    class_name: '电影排行&电视剧排行&综艺排行',
    class_url: 'movies&tv&variety',
    
    searchable: 1,
    quickSearch: 1,
    filterable: 0,
    
    headers: {
        'User-Agent': 'Mozilla/5.0'
    },
    
    play_parse: true,
    limit: 50,
    
    推荐: async function () {
        let url = this.host + '/movies.json';
        let html = await request(url);
        let data = JSON.parse(html);
        return data.slice(0, 50).map(item => ({
            vod_id: item.vod_id,
            vod_name: item.vod_name,
            vod_pic: item.vod_pic,
            vod_remarks: item.vod_remarks || item.score + '分'
        }));
    },
    
    一级: async function (tid, pg, filter, extend) {
        let url = this.host + `/${tid}.json`;
        let html = await request(url);
        let data = JSON.parse(html);
        return data.list.map(item => ({
            vod_id: item.vod_id,
            vod_name: item.vod_name,
            vod_pic: item.vod_pic,
            vod_remarks: item.vod_remarks
        }));
    },
    
    二级: async function (ids) {
        let files = ['movies.json', 'tv.json', 'variety.json'];
        let vod = null;
        for (let file of files) {
            let url = this.host + `/${file}`;
            let html = await request(url);
            let data = JSON.parse(html);
            vod = data.find(item => item.vod_id == ids[0]);
            if (vod) break;
        }
        if (!vod) return {list: []};
        return {
            list: [{
                vod_id: vod.vod_id,
                vod_name: vod.vod_name,
                vod_pic: vod.vod_pic,
                vod_content: vod.content || '',
                vod_play_from: vod.vod_play_from || 'default',
                vod_play_url: vod.vod_play_url || ''
            }]
        };
    },
    
    搜索: async function (wd, quick, pg) {
        let results = [];
        let files = ['movies.json', 'tv.json', 'variety.json'];
        for (let file of files) {
            let url = this.host + `/${file}`;
            let html = await request(url);
            let data = JSON.parse(html);
            let filtered = data.filter(item => 
                item.vod_name && item.vod_name.includes(wd)
            );
            results = results.concat(filtered.map(item => ({
                vod_id: item.vod_id,
                vod_name: item.vod_name,
                vod_pic: item.vod_pic,
                vod_remarks: item.vod_remarks
            })));
        }
        return results;
    },
    
    lazy: async function (flag, id) {
        return {parse: 0, url: id};
    }
}
