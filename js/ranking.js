var rule = {
    类型: '影视',
    title: '📊 豆瓣榜单',
    host: 'https://caiji.dbzy5.com',
    
    class_name: '电影&电视剧&综艺',
    class_url: '1&2&3',
    
    searchable: 1,
    quickSearch: 1,
    filterable: 0,
    
    headers: {
        'User-Agent': 'Mozilla/5.0'
    },
    
    play_parse: true,
    limit: 50,
    
    推荐: async function () {
        let url = this.host + '/api.php/provide/vod/at/json/?ac=detail&pg=1';
        let html = await request(url);
        let data = JSON.parse(html);
        return data.list.slice(0, 50).map(item => ({
            vod_id: item.vod_id,
            vod_name: item.vod_name,
            vod_pic: item.vod_pic,
            vod_remarks: item.vod_douban_score ? item.vod_douban_score + '分' : item.vod_remarks
        }));
    },
    
    一级: async function (tid, pg, filter, extend) {
        let url = this.host + `/api.php/provide/vod/at/json/?ac=detail&t=${tid}&pg=${pg}`;
        let html = await request(url);
        let data = JSON.parse(html);
        return data.list.map(item => ({
            vod_id: item.vod_id,
            vod_name: item.vod_name,
            vod_pic: item.vod_pic,
            vod_remarks: item.vod_douban_score ? item.vod_douban_score + '分' : item.vod_remarks
        }));
    },
    
    二级: async function (ids) {
        let url = this.host + `/api.php/provide/vod/at/json/?ac=detail&ids=${ids[0]}`;
        let html = await request(url);
        let data = JSON.parse(html);
        let vod = data.list[0];
        return {
            list: [{
                vod_id: vod.vod_id,
                vod_name: vod.vod_name,
                vod_pic: vod.vod_pic,
                vod_content: vod.vod_content || '',
                vod_play_from: vod.vod_play_from || 'default',
                vod_play_url: vod.vod_play_url || ''
            }]
        };
    },
    
    搜索: async function (wd, quick, pg) {
        let url = this.host + `/api.php/provide/vod/at/json/?ac=detail&wd=${encodeURIComponent(wd)}&pg=${pg}`;
        let html = await request(url);
        let data = JSON.parse(html);
        return data.list.map(item => ({
            vod_id: item.vod_id,
            vod_name: item.vod_name,
            vod_pic: item.vod_pic,
            vod_remarks: item.vod_douban_score ? item.vod_douban_score + '分' : item.vod_remarks
        }));
    },
    
    lazy: async function (flag, id) {
        return {parse: 0, url: id};
    }
}
