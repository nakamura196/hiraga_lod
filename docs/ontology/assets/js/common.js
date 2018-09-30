// Prefix
var prefixes = new Object();
prefixes["dc"] = "http://purl.org/dc/elements/1.1/";
prefixes["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
prefixes["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#";
prefixes["foaf"] = "http://xmlns.com/foaf/0.1/";
prefixes["kd"] = "http://kashiwade.org/2012/09/kd#";
prefixes["dcterms"] = "http://purl.org/dc/terms/";
prefixes["owl"] = "http://www.w3.org/2002/07/owl#";
prefixes["kdclass"] = "http://kashiwade.org/2012/09/kd/class/";
prefixes["kdinstance"] = "http://kashiwade.org/2012/09/kd/entity/";
prefixes["text"] = "http://jena.apache.org/text#";
prefixes["geo"] = "http://www.w3.org/2003/01/geo/wgs84_pos#";
prefixes["xsd"] = "http://www.w3.org/2001/XMLSchema#";
prefixes["cal"] = "http://www.w3.org/2002/12/cal/icaltzd#";
prefixes["dcndl"] = "http://ndl.go.jp/dcndl/terms/";
prefixes["hm"] = "http://apps.is.k.u-tokyo.ac.jp/hiraga/property#";
prefixes["dbo"] = "http://dbpedia.org/ontology/";
prefixes["dbp"] = "http://dbpedia.org/property/";
prefixes["dbp-ja"] = "http://ja.dbpedia.org/property/";

function getPrefixes() {
	var prefix = "\r\n";
	$.each(prefixes, function(key, value) {
		prefix += " PREFIX " + key + ": <" + value + ">  \r\n";
	});
	return prefix;
}

var endpoint = "https://dydra.com/ut-digital-archives/hiraga_lod/sparql"

// Graph URI
var graphs = new Object();
graphs.shipOntologyLocation = "http://apps.is.k.u-tokyo.ac.jp/hiraga/ship_ontology#location";
graphs.shipTree = "http://apps.is.k.u-tokyo.ac.jp/hiraga/ship_ontologyhand/201708/";// 階層関係
graphs.timeline = "http://apps.is.k.u-tokyo.ac.jp/hiraga/timeline";
graphs["timeline-keyword"] = "http://apps.is.k.u-tokyo.ac.jp/hiraga/timeline_keyword";

function arrangeDate(date) {
  var str = date.split("-");
  var year = str[0];
  var obj = seirekiToWareki_2(year);

  var dateStr = obj.era + obj.year + "（" + year + "）年";

  // 月が存在する場合
  if (str[1] != null) {
    dateStr += Number(str[1]) + "月";
  }

  // 日が存在する場合
  if (str[2] != null) {
    dateStr += Number(str[2]) + "日";
  }

  return dateStr;
}

/**
* 西暦年から和暦記号・年を抽出するメソッド
*
* @param year
* @returns {___anonymous5833_5835}
*/
function seirekiToWareki_2(year) {

  year = Number(year);

  var obj = new Object();
  if (year > 1988) {
    obj.era = getWareki(4);
    obj.year = parseInt(year) - 1988;
  } else if (year > 1925) {
    obj.era = getWareki(3);
    obj.year = parseInt(year) - 1925;
  } else if (year > 1911) {
    obj.era = getWareki(2);
    obj.year = parseInt(year) - 1911;
  } else if (year > 1867) {
    obj.era = getWareki(1);
    obj.year = parseInt(year) - 1867;
  } else {
    obj.era = 0;
    obj.year = year;
  }
  return obj;
}

/**
* 和暦記号から和暦を抽出するメソッド
*
* @param era
* @returns
*/
function getWareki(era) {
  if (era == 1) {
    return "明治";
  } else if (era == 2) {
    return "大正";
  } else if (era == 3) {
    return "昭和";
  } else if (era == 4) {
    return "平成";
  } else {
    return null;
  }
}
