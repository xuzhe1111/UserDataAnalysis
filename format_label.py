import sys

from label_cluster import ClusterHandler

def load_dataset(input_stream):
  doc_list = []
  pre_query = None
  for line in input_stream:
    line = line.rstrip('\n')
    fields = line.split('\t')
    if len(fields) < 2:
      print >> sys.stderr, "Failed for line format error:%s" % line
      continue

    query_id = fields[1]
    label = float(fields[0])
    feature = '\t'.join(fields[1:])

    if pre_query is None:
      pre_query = query_id

    if pre_query == query_id:
      doc_list.append((label, feature))
    else:
      format_label(doc_list)

      doc_list = []
      doc_list.append((label, feature))
      pre_query = query_id

  format_label(doc_list)

def sum_norm(score_list):
    sum_score = sum(score_list)
    if sum_score <= 0:
      return

    norm_list = []
    for score in score_list:
      norm_list.append(score/sum_score)

    return norm_list


def format_label(doc_list):
  doc_list.sort(key=lambda item:item[0], reverse=True)
  score_list = []
  for doc in doc_list:
    score, feature = doc
    score_list.append(score)

  score_list = sum_norm(score_list)
  if not score_list:
    return

  cluster_handler = ClusterHandler()
  label_list = cluster_handler.do_cluster(score_list)
  if len(score_list) != len(label_list):
    print >> sys.stderr, "Error for label list size error."
    return

  for i in range(len(doc_list)):
    label, feature = label_list[i], doc_list[i][1]
    print '%s\t%s' % (label, feature)

if __name__ == '__main__':
  load_dataset(sys.stdin)
