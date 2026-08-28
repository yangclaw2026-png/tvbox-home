var rule = {
	title: '玩偶哥哥',
	类型: '影视',
	host: 'https://wogg.link',
	headers: {
		'User-Agent': 'MOBILE_UA'
	},
	timeout: 5000,
	class_name: '电影&电视剧&动漫&综艺&短剧',
	class_url: '1&2&3&4&6',
	searchable: 2,
	quickSearch: 0,
	filterable: 0,
	play_parse: true,
	play_json: [{
		re: '*',
		json: {
			parse: 0,
			jx: 0
		}
	}],
	lazy: '',
	limit: 6,
	推荐: `js:
		var d = [];
		let html = request(HOST);
		let list = pdfa(html, '.module-item');
		list.forEach(it => {
			d.push({
				title: pdfh(it, 'a&&title'),
				img: pd(it, '.module-item-pic&&img&&data-src'),
				desc: pdfh(it, '.module-item-text&&Text'),
				url: pd(it, 'a&&href')
			});
		});
		setResult(d);
	`,
	一级: `js:
		var d = [];
		let tUrl = HOST + '/vodshow/' + MY_CATE + '--------' + MY_PAGE + '---.html';
		let html = request(tUrl);
		let list = pdfa(html, '.module-item');
		list.forEach(it => {
			d.push({
				title: pdfh(it, 'a&&title'),
				img: pd(it, '.module-item-pic&&img&&data-src'),
				desc: pdfh(it, '.module-item-text&&Text'),
				url: pd(it, 'a&&href')
			});
		});
		setResult(d);
	`,
	二级: `js:
		try {
			let html = request(MY_URL);
			VOD = {
				vod_id: MY_URL,
				vod_name: pdfh(html, 'h1&&Text'),
				vod_pic: pd(html, '.player-poster&&src'),
				vod_content: pdfh(html, '.video-info-content&&p,-1&&Text'),
				vod_actor: pdfh(html, '.video-info-main&&.video-info-actor,1&&Text'),
				vod_director: '',
				vod_year: '',
				vod_area: '',
				type_name: ''
			};
			let playFrom = ['网盘资源'];
			let playList = [];
			let links = pdfa(html, '.module-row-one');
			let plays = [];
			links.forEach(it => {
				let title = pdfh(it, 'h4&&Text');
				let url = pd(it, '.btn-down&&a&&href');
				if (url && url.indexOf('http') === 0) {
					plays.push(title + '$' + url);
				}
			});
			if (plays.length > 0) {
				playList.push(plays.join('#'));
			}
			VOD.vod_play_from = playFrom.join('$$$');
			VOD.vod_play_url = playList.join('$$$');
		} catch(e) {
			log('玩偶哥哥二级:' + e.message);
		}
	`,
	搜索: `js:
		var d = [];
		let sUrl = HOST + '/vodsearch/-------------.html?wd=' + encodeURIComponent(KEY) + '&page=' + MY_PAGE;
		let html = request(sUrl);
		let list = pdfa(html, '.module-search-item');
		list.forEach(it => {
			d.push({
				title: pdfh(it, 'h3&&Text'),
				img: pd(it, '.lazyload&&data-src'),
				desc: pdfh(it, '.video-info&&a&&Text'),
				url: pd(it, 'h3&&a&&href')
			});
		});
		setResult(d);
	`,
}
