import os
import argparse
import numpy as np
import torch
import pickle as pkl

import matplotlib.pyplot as plt

from TSX.utils import load_data

# feature_map_mimic = ['ANION GAP', 'ALBUMIN', 'BICARBONATE', 'BILIRUBIN', 'CREATININE', 'CHLORIDE', #'GLUCOSE',
#                      'HEMATOCRIT', 'HEMOGLOBIN', 'LACTATE', 'MAGNESIUM', 'PHOSPHATE', 'PLATELET', 'POTASSIUM',
#                      'PTT', 'INR', 'PT', 'SODIUM', 'BUN', 'WBC', 'HeartRate', 'SysBP' , 'DiasBP' , 'MeanBP' ,
#                      'RespRate' , 'SpO2' , 'Glucose','Temp']
feature_map_mimic = ['ANION GAP (mEq/L)', 'ALBUMIN (g/dL)', 'BICARBONATE (mEq/L)', 'BILIRUBIN (mg/dL)', 'CREATININE (mg/dL)',
                     'CHLORIDE (mEq/L)', 'HEMATOCRIT (%)', 'HEMOGLOBIN (g/dL)', 'LACTATE (mmol/L)', 'MAGNESIUM (mmol/L)',
                     'PHOSPHATE (mg/dL)', 'PLATELET (K/uL)', 'POTASSIUM (mEq/L)', 'PTT', 'INR', 'PT (sec)',
                     'SODIUM (mEq/L == mmol/L)', 'BUN', 'WBC', 'HeartRate', 'SysBP' , 'DiasBP' , 'MeanBP' , 'RespRate' ,
                     'SpO2' , 'Glucose','Temp (degC)']

top_patients = [3095]#, 1534, 3663, 4126, 3734, 82, 2604, 3305, 870, 2733, 3319, 1057, 1575, 1484, 1672, 720, 3509, 2599,
                # 3783, 2015, 1419, 4127, 2776, 3324, 462, 3184, 4015, 2104, 3226, 811, 3510, 2141, 1987, 4537, 4271, 973,
                # 1961, 1239, 3368, 4469, 3586, 1645, 1103, 816, 756, 906, 897, 2461, 259, 4110, 3179, 2135, 3344, 1749]#,
                # 3347, 3188, 3286, 3437, 3656, 2154, 3782, 1993, 3060, 4397, 4236, 589, 1936, 2522, 2291, 4301, 3644,
                # 2455, 1191, 2439, 4514, 3041, 4538, 8, 3168, 165, 3567, 299, 1935, 3373, 4489, 1773, 2112, 4220, 3609]




    # labels = np.zeros((x.shape[0], x.shape[-1]))
    # for t in range(1, x.shape[-1]):
    #     if args.explainer=='retain':
    #         x_retain = x.permute(0, 2, 1)
    #         p_y_t, _, _ = explainer.base_model(x_retain[:, :t + 1, :], (torch.ones((len(x),)) * t+1))
    #     else:
    #         p_y_t = explainer.base_model(x[:, :, :t + 1], return_multi=True)
    #     labels[:, t - 1] = np.array([p > 0.5 for p in p_y_t.cpu().detach().numpy()[:, 1]]).flatten()
        #print(np.any(np.isnan(gt_importance_test)), np.any(np.isnan(ranked_features)), np.any(np.isnan(score)))
    # break


## This part is copied from baselin.plots. It can be reused, we only need to read the scores from the pkl files
    # Print results
    # plot_ids = [13]#np.random.randint(200, size=10)
    #
    # for plot_id in plot_ids:
    #     f, axs = plt.subplots(3)
    #     f.set_figheight(6)
    #     f.set_figwidth(10)
    #     score_pd = pd.DataFrame(columns=['f1', 'f2', 'f3', 's1', 's2', 's3'])
    #     score_pd['t'] = pd.Series(np.arange(1, score[plot_id].shape[-1]))
    #     cmap = sns.cubehelix_palette(rot=.2, as_cmap=True)
    #     bottom = cm.get_cmap('Blues', 128)
    #     for feat in [1, 2, 3]:  # range(1,2):
    #         score_pd['f%d' % feat] = pd.Series(x[plot_id, feat - 1, 1:].cpu().numpy())
    #         score_pd['s%d' % feat] = pd.Series(score[plot_id, feat - 1, :])
    #         f = interpolate.interp1d(score_pd['t'], score_pd['f%d' % feat], fill_value="extrapolate")
    #         f_score = interpolate.interp1d(score_pd['t'], score_pd['s%d' % feat], fill_value="extrapolate")
    #         xnew = np.arange(1, score[plot_id].shape[-1] - 0.99, 0.01)
    #         ynew = f(xnew)
    #         score_new = f_score(xnew)
    #         # axs[feat-1].scatter(xnew, ynew, c=cm.hot(score_new/2.+0.5), edgecolor='none')
    #         axs[feat - 1].scatter(xnew, ynew, c=bottom(score_new / 2. + 0.5), edgecolor='none')
    #     plt.legend()
    #     plt.savefig(os.path.join(plot_path, 'new_viz.pdf'), dpi=300, orientation='landscape')
    #
    #     t_len = score[plot_id].shape[-1]
    #     f, axs = plt.subplots(3)
    #
    #     # plot_heatmap_text(ranked_features[plot_id, :, 1:], score[plot_id, :, 1:],
    #     #                   os.path.join(plot_path, '%s_example_heatmap.pdf' % args.explainer), axs[2])
    #     t = np.arange(1, t_len)
    #
    #     # pred_batch_vec = []
    #     # model.eval()
    #     # for tt in t:
    #     #     pred_tt = model(x[plot_id, :, :tt + 1].unsqueeze(0)).detach().cpu().numpy()
    #     #     # pred_tt = np.argmax(pred_tt, -1)
    #     #     pred_tt = pred_tt[:,-1]
    #     #     pred_batch_vec.append(pred_tt)
    #
    #
    #     if data_type == 'state':
    #
    #         shade_state_state_data(state_test[plot_id], t, axs[0])
    #         '''
    #         if args.gt == 'pred_model':
    #             for tt in t:
    #                 if tt>1:
    #                     label_change = abs((pred_batch_vec[tt-1][:,1]-pred_batch_vec[tt-2][:,1]).reshape(-1,1))
    #                     gt_importance_test[:,:,tt-1] = np.multiply(np.repeat(label_change,x.shape[1],axis=1), \
    #                     gt_importance_test[:,:,tt-1])
    #         elif args.gt == 'true_model':
    #             for tt in t:
    #                 if tt>1:
    #                     label_change = abs((y[:,tt-1]-y[:,tt-2]).cpu().detach().numpy().reshape(-1,1))
    #                     gt_importance_test[:,:,tt-1] = np.multiply(np.repeat(label_change,x.shape[1],axis=1), \
    #                     gt_importance_test[:,:,tt-1])
    #
    #                     logits_change = abs((logits_test[:,tt-1]-logits_test[:,tt-2]).reshape(-1,1))
    #                     gt_soft_score[:,:,tt-1] = np.multiply(np.repeat(logits_change,x.shape[1],axis=1), \
    #                     gt_importance_test[:,:,tt-1])
    #         '''
    #     if data_type == 'mimic':
    #         max_scores = np.array(x[plot_id, :, 1:]).max(axis=-1)
    #         top_features = max_scores.argsort()[-4:][::-1]
    #     else:
    #         top_features = list(np.range(x.shape[1]))
    #
    #     for i, ref_ind in enumerate(range(x[plot_id].shape[0])):
    #         if ref_ind in top_features:
    #             plt_label = '%s'%feature_map_mimic[ref_ind] if data_type=='mimic' else 'feature %d' % (i)
    #             axs[0].plot(t, x[plot_id, ref_ind, 1:].cpu().numpy(), linewidth=3, label=plt_label)#'feature %d' % (i))
    #             axs[1].plot(t, score[plot_id, ref_ind, 1:], linewidth=3, label=plt_label)#'importance %d' % (i))
    #         # if args.explainer == 'fit':
    #         #     axs[3].plot(t,
    #         #                 score_mean_shift[plot_id, ref_ind, 1:], linewidth=3, label='importance %d' % (i))
    #
    #     # axs[0].plot(t, pred_batch_vec, '--', linewidth=3, c='black')
    #     # axs[0].plot(t, y[plot_id, 1:].cpu().numpy(), '--', linewidth=3, c='red')
    #     axs[0].tick_params(axis='both', labelsize=20)
    #     axs[2].tick_params(axis='both', labelsize=20)
    #     axs[1].tick_params(axis='both', labelsize=20)
    #     axs[1].set_title('%s'%args.explainer, fontsize=30)
    #     axs[0].margins(0.03)
    #     axs[2].margins(0.03)
    #     axs[1].margins(0.03)
    #
    #     # axs[0].grid()
    #     f.set_figheight(16)
    #     f.set_figwidth(24)
    #     plt.subplots_adjust(hspace=.5)
    #     name = args.explainer + '_' + args.generator_type if args.explainer == 'fit' else args.explainer
    #     # print('**************', int(y[plot_id]))
    #     plt.savefig(os.path.join(plot_path, '%s_example_%d_%s.pdf' %(name, plot_id, ['survived', 'dead'][int(y[plot_id])])), dpi=300, orientation='landscape')
    #     fig_legend = plt.figure(figsize=(13, 1.2))
    #     handles, labels = axs[0].get_legend_handles_labels()
    #     plt.figlegend(handles, labels, loc='upper left', ncol=4, fancybox=True, handlelength=6, fontsize='xx-large')
    #     fig_legend.savefig(os.path.join(plot_path, '%s_example_legend_%d_%s.pdf'%(name, plot_id, ['survived', 'dead'][int(y[plot_id])])), dpi=300, bbox_inches='tight')




if __name__ == '__main__':
    np.random.seed(1234)
    parser = argparse.ArgumentParser(description='Run baseline model for explanation')
    parser.add_argument('--explainer', type=str, default='fit', help='Explainer model')
    parser.add_argument('--data', type=str, default='simulation')
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--train_gen', action='store_true')
    parser.add_argument('--generator_type', type=str, default='history')
    parser.add_argument('--binary', action='store_true', default=False)
    parser.add_argument('--gt', type=str, default='true_model', help='specify ground truth score')
    parser.add_argument('--cv', type=int, default=1)
    args = parser.parse_args()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'


    if args.data == 'simulation':
        feature_size = 3
        data_path = './data/simulated_data'
        data_type='state'
    elif args.data == 'simulation_l2x':
        feature_size = 3
        data_path = './data/simulated_data_l2x'
        data_type='state'
    elif args.data == 'simulation_spike':
        feature_size = 3
        data_path = './data/simulated_spike_data'
        data_type='spike'
    elif args.data == 'mimic':
        data_type = 'mimic'
        timeseries_feature_size = len(feature_map_mimic)

    output_path = '/scratch/gobi1/sana/TSX_results/new_results/%s' % args.data
    with open(os.path.join(output_path, '%s_test_importance_scores_%d.pkl' % (args.explainer, args.cv)), 'wb') as f:
        importance_scores = pkl.load(f)


    if args.data == 'mimic':
        # Plot patient summary sheet
        p_data, train_loader, valid_loader, test_loader = load_data(batch_size=100, path='./data', transform=None, cv=0)
        testset = list(test_loader.dataset)
        x_test = torch.stack(([x[0] for x_ind, x in enumerate(testset) if x_ind in top_patients])).cpu().numpy()
        y_test = torch.stack(([x[1] for x_ind, x in enumerate(testset) if x_ind in top_patients])).cpu().numpy()

        for j, x in enumerate(x_test):
            pid = top_patients[j]
            fig = plt.figure(constrained_layout=True)
            gs = fig.add_gridspec(8, 2)
            fig.set_figheight(16)
            fig.set_figwidth(24)
            axs_table = fig.add_subplot(gs[:, 1])
            axs_table.set_title('lab results', fontsize=24)

            # Initialize the vertical-offset for the stacked bar chart.
            y_offset = 1
            columns = range(0, 49, 4)
            # Plot bars and create text labels for the table
            cell_text = []
            bar_width = 6
            bar_heigth = 1.5
            for row in range(19):
                cell_text.append([meas for i, meas in enumerate(x[row, :]) if i % 4 == 0])
            the_table = axs_table.table(cellText=cell_text,
                                        rowLabels=feature_map_mimic[:19],
                                        colLabels=columns,
                                        loc='center')
            the_table.scale(0.4, 3)
            the_table.set_fontsize(24)
            axs_table.axis("off")

            # f, axs = plt.subplots(8)
            ethnicity = ['unknown', 'white', 'black', 'hispanic', 'asian', 'other'][
                int(x[len(feature_map_mimic) + 2, 0])]
            gender = ['Male', 'Female'][int(x[len(feature_map_mimic), 0])]
            fig.suptitle(
                'Gender:%s \t Age: %d \t Ethnicity: %s' % (gender, x[len(feature_map_mimic) + 1, 0], ethnicity),
                fontsize=24)
            axs = []
            for i, sig in enumerate(range(19, len(feature_map_mimic))):
                ax = fig.add_subplot(gs[i, 0])
                axs.append(ax)
                axs[i].plot(x[sig, :], 'x')
                axs[i].set_title(feature_map_mimic[sig], fontsize=24)
            plt.savefig('./plots/mimic_clinical_eval/sample_%d.pdf' % pid)

        # Plot importance scores